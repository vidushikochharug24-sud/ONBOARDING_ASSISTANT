from flask import Blueprint, request, jsonify
from groq import Groq
from supabase import create_client
from auth import verify_token
import os
import threading
import requests
import zipfile
import io
import json

from rag import embed_and_store_github, embed_and_store_zip

analyze_bp = Blueprint("analyze", __name__)

groq_client = Groq()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

MODEL = "llama-3.3-70b-versatile"
BUCKET = "codebase-files"


def fetch_github_repo(url):
    """Fetch file tree and key files from a GitHub repo URL"""
    # Extract owner/repo from URL
    parts = url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    if repo.endswith(".git"):
        repo = repo[:-4]

    headers = {"Accept": "application/vnd.github.v3+json"}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    # Get repo tree
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    tree_resp = requests.get(tree_url, headers=headers)
    if tree_resp.status_code != 200:
        return None, "Could not fetch repo. Make sure it's public."

    tree = tree_resp.json().get("tree", [])
    file_paths = [f["path"] for f in tree if f["type"] == "blob"]

    # Get README
    readme_content = ""
    for readme_name in ["README.md", "readme.md", "README.txt"]:
        r = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/contents/{readme_name}",
            headers=headers
        )
        if r.status_code == 200:
            import base64
            readme_content = base64.b64decode(r.json()["content"]).decode("utf-8", errors="ignore")[:3000]
            break

    # Get key config files
    key_files_content = {}
    for fname in ["package.json", "requirements.txt", "pom.xml", "Cargo.toml", "go.mod", "Dockerfile"]:
        if fname in file_paths:
            r = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/contents/{fname}",
                headers=headers
            )
            if r.status_code == 200:
                import base64
                key_files_content[fname] = base64.b64decode(r.json()["content"]).decode("utf-8", errors="ignore")[:1000]

    return {
        "repo_name": f"{owner}/{repo}",
        "file_tree": file_paths[:200],
        "readme": readme_content,
        "key_files": key_files_content
    }, None


def extract_zip_contents(file_path):
    """Download ZIP from Supabase and extract file tree + content"""
    file_bytes = supabase.storage.from_(BUCKET).download(file_path)
    zip_file = zipfile.ZipFile(io.BytesIO(file_bytes))

    file_list = zip_file.namelist()
    contents = {}

    # Read key files
    for name in file_list:
        lower = name.lower()
        if any(lower.endswith(ext) for ext in [
            "readme.md", "readme.txt", "package.json",
            "requirements.txt", "dockerfile", ".env.example"
        ]):
            try:
                contents[name] = zip_file.read(name).decode("utf-8", errors="ignore")[:2000]
            except Exception:
                pass

    return {
        "file_tree": file_list[:200],
        "key_files": contents
    }


def extract_pdf_text(file_path):
    """Download PDF from Supabase and extract text"""
    file_bytes = supabase.storage.from_(BUCKET).download(file_path)

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            text = ""
            for page in pdf.pages[:10]:  # first 10 pages
                text += page.extract_text() or ""
        return text[:5000]
    except Exception as e:
        return f"Could not extract PDF text: {str(e)}"


def build_analysis_prompt(source_type, source_data, doc_text=""):
    base = f"""You are a senior staff engineer helping a new team member onboard to a codebase.

Analyze the following codebase information and generate a comprehensive "New Engineer Onboarding Guide".

SOURCE TYPE: {source_type}
"""
    if source_type == "github":
        base += f"""
REPOSITORY: {source_data.get('repo_name')}

FILE TREE (first 200 files):
{chr(10).join(source_data.get('file_tree', []))}

README:
{source_data.get('readme', 'No README found')}

KEY CONFIG FILES:
{json.dumps(source_data.get('key_files', {}), indent=2)}
"""
    elif source_type == "zip":
        base += f"""
FILE TREE:
{chr(10).join(source_data.get('file_tree', []))}

KEY FILES CONTENT:
{json.dumps(source_data.get('key_files', {}), indent=2)}
"""

    if doc_text:
        base += f"""
ADDITIONAL INTERNAL DOCUMENTATION:
{doc_text[:3000]}
"""

    base += """
Generate a structured onboarding guide with these sections:

1. **What This Project Does** - Plain English explanation (2-3 sentences)
2. **Tech Stack** - List all technologies detected with their purpose
3. **Project Structure** - Explain the folder structure and what each major folder/file does
4. **Key Files to Know** - The 5-7 most important files a new engineer should read first
5. **How to Get Started** - Step by step setup instructions based on what you see
6. **Architecture Overview** - How the main components connect and interact
7. **Where to Start Contributing** - Which files/folders to look at for different types of tasks
8. **Common Gotchas** - Potential pain points or things that might trip up a new engineer

Be specific, practical, and use the actual file names and folder names you see. Write as if you're a helpful senior engineer, not a generic AI.
"""
    return base


@analyze_bp.route("/github", methods=["POST"])
def analyze_github():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    url = data.get("url", "")
    doc_file_path = data.get("doc_file_path", "")

    if not url:
        return jsonify({"error": "GitHub URL required"}), 400

    source_data, error = fetch_github_repo(url)
    if error:
        return jsonify({"error": error}), 400

    doc_text = ""
    if doc_file_path:
        doc_text = extract_pdf_text(doc_file_path)

    prompt = build_analysis_prompt("github", source_data, doc_text)

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.3
    )

    guide = response.choices[0].message.content

    # Save guide to DB
    record = supabase.table("onboarding_guides").insert({
        "workspace_id": payload["workspace_id"],
        "source_type": "github",
        "source_url": url,
        "guide_content": guide,
        "repo_name": source_data.get("repo_name", url)
    }).execute()

    thread = threading.Thread(
        target=embed_and_store_github,
        args=(payload["workspace_id"], record.data[0]["id"], url)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "guide": guide,
        "guide_id": record.data[0]["id"],
        "repo_name": source_data.get("repo_name", url),
        "source_type": "github",
        "created_at": record.data[0].get("created_at")
    })


@analyze_bp.route("/zip", methods=["POST"])
def analyze_zip():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    file_path = data.get("file_path", "")
    doc_file_path = data.get("doc_file_path", "")
    repo_name = data.get("repo_name", "Uploaded Codebase")

    if not file_path:
        return jsonify({"error": "file_path required"}), 400

    source_data = extract_zip_contents(file_path)

    doc_text = ""
    if doc_file_path:
        doc_text = extract_pdf_text(doc_file_path)

    prompt = build_analysis_prompt("zip", source_data, doc_text)

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.3
    )

    guide = response.choices[0].message.content

    record = supabase.table("onboarding_guides").insert({
        "workspace_id": payload["workspace_id"],
        "source_type": "zip",
        "source_url": file_path,
        "guide_content": guide,
        "repo_name": repo_name
    }).execute()

    thread = threading.Thread(
        target=embed_and_store_zip,
        args=(payload["workspace_id"], record.data[0]["id"], file_path)
    )
    thread.daemon = True
    thread.start()

    return jsonify({
        "guide": guide,
        "guide_id": record.data[0]["id"],
        "repo_name": repo_name,
        "source_type": "zip",
        "created_at": record.data[0].get("created_at")
    })


@analyze_bp.route("/guides", methods=["GET"])
def list_guides():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    guides = supabase.table("onboarding_guides").select(
        "id, repo_name, source_type, created_at"
    ).eq("workspace_id", payload["workspace_id"]).order("created_at", desc=True).execute()

    return jsonify(guides.data)


@analyze_bp.route("/guides/<guide_id>", methods=["GET"])
def get_guide(guide_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Unauthorized"}), 401

    guide = supabase.table("onboarding_guides").select("*").eq(
        "id", guide_id
    ).eq("workspace_id", payload["workspace_id"]).execute()

    if not guide.data:
        return jsonify({"error": "Guide not found"}), 404

    return jsonify(guide.data[0])
