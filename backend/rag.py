from sentence_transformers import SentenceTransformer
from supabase import create_client
from groq import Groq
import os
import requests
import base64
import zipfile
import io

# Load embedding model (runs locally, free)
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # 384 dimensions, fast and good

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)
groq_client = Groq()
MODEL = "llama-3.3-70b-versatile"

# File extensions worth embedding
CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp", ".c",
    ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".cs",
    ".html", ".css", ".md", ".json", ".yaml", ".yml", ".env.example"
}

def should_embed(filename):
    return any(filename.endswith(ext) for ext in CODE_EXTENSIONS)


def chunk_text(text, filename, chunk_size=500):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    step = chunk_size - 50  # 50 word overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append({
                "file_path": filename,
                "content": chunk
            })

    return chunks


def embed_and_store_github(workspace_id, guide_id, repo_url):
    """Fetch GitHub repo files, embed them, store in pgvector"""
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    if repo.endswith(".git"):
        repo = repo[:-4]

    headers = {"Accept": "application/vnd.github.v3+json"}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    # Get file tree
    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    tree_resp = requests.get(tree_url, headers=headers)
    if tree_resp.status_code != 200:
        return False

    tree = tree_resp.json().get("tree", [])
    embeddable = [f for f in tree if f["type"] == "blob" and should_embed(f["path"])][:30]  # limit 30 files

    all_chunks = []
    for file_info in embeddable:
        file_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_info['path']}"
        resp = requests.get(file_url, headers=headers)
        if resp.status_code != 200:
            continue
        try:
            content = base64.b64decode(resp.json()["content"]).decode("utf-8", errors="ignore")
            chunks = chunk_text(content, file_info["path"])
            all_chunks.extend(chunks)
        except Exception:
            continue

    _store_chunks(workspace_id, guide_id, all_chunks)
    return True


def embed_and_store_zip(workspace_id, guide_id, file_path):
    """Extract ZIP from Supabase, embed files, store in pgvector"""
    file_bytes = supabase.storage.from_("codebase-files").download(file_path)
    zip_file = zipfile.ZipFile(io.BytesIO(file_bytes))

    all_chunks = []
    embeddable = [f for f in zip_file.namelist() if should_embed(f)][:30]

    for name in embeddable:
        try:
            content = zip_file.read(name).decode("utf-8", errors="ignore")
            chunks = chunk_text(content, name)
            all_chunks.extend(chunks)
        except Exception:
            continue

    _store_chunks(workspace_id, guide_id, all_chunks)
    return True


def _store_chunks(workspace_id, guide_id, chunks):
    """Generate embeddings and store in Supabase pgvector"""
    if not chunks:
        return

    texts = [c["content"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=False)

    rows = []
    for i, chunk in enumerate(chunks):
        rows.append({
            "workspace_id": workspace_id,
            "guide_id": guide_id,
            "file_path": chunk["file_path"],
            "content": chunk["content"],
            "embedding": embeddings[i].tolist()
        })

    # Insert in batches of 20
    for i in range(0, len(rows), 20):
        batch = rows[i:i+20]
        supabase.table("code_chunks").insert(batch).execute()


def search_chunks(workspace_id, guide_id, question, top_k=3):
    """Find most relevant chunks for a question using cosine similarity"""
    question_embedding = embedder.encode([question])[0].tolist()

    # Use Supabase RPC for vector similarity search
    result = supabase.rpc("match_code_chunks", {
        "query_embedding": question_embedding,
        "match_workspace_id": workspace_id,
        "match_guide_id": guide_id,
        "match_count": top_k
    }).execute()

    return result.data or []


def get_guide_content(guide_id, workspace_id):
    """Fetch the saved guide content as a fallback source of context."""
    result = supabase.table("onboarding_guides").select(
        "id, guide_content, repo_name, source_type, created_at"
    ).eq("id", guide_id).eq("workspace_id", workspace_id).limit(1).execute()

    if not result.data:
        return None

    return result.data[0]


def chat_with_codebase(workspace_id, guide_id, question, conversation_history):
    """RAG chat - find relevant chunks and answer the question"""
    # Search for relevant code chunks
    relevant_chunks = search_chunks(workspace_id, guide_id, question)
    guide = get_guide_content(guide_id, workspace_id)

    if not relevant_chunks:
        context = "No specific code context found."
    else:
        context = "\n\n---\n\n".join([
            f"File: {chunk['file_path']}\n{chunk['content'][:500]}"
            for chunk in relevant_chunks
        ])

    guide_context = ""
    if guide and guide.get("guide_content"):
        guide_context = f"\n\nGUIDE CONTENT:\n{guide['guide_content']}"

    system_prompt = f"""You are a helpful senior engineer who knows this codebase deeply.
Answer questions based on the actual code provided below.
Be specific, reference actual file names and code when relevant.
If the code context doesn't contain the answer, say so honestly.

RELEVANT CODE CONTEXT:
{context}{guide_context}
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": question})

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.3
    )

    return response.choices[0].message.content
