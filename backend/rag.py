import os
import requests
import zipfile
import io
import base64
from supabase import create_client
from groq import Groq

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)
groq_client = Groq()
MODEL = "llama-3.3-70b-versatile"

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_EMBED_URL = "https://api.cohere.ai/v1/embed"

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".cpp", ".c",
    ".go", ".rs", ".rb", ".php", ".swift", ".kt", ".cs",
    ".html", ".css", ".md", ".json", ".yaml", ".yml"
}

def should_embed(filename):
    return any(filename.endswith(ext) for ext in CODE_EXTENSIONS)


def get_embeddings(texts, input_type="search_document"):
    """Call Cohere API to get embeddings - 1024 dimensions"""
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        COHERE_EMBED_URL,
        headers=headers,
        json={
            "texts": texts,
            "model": "embed-english-light-v3.0",
            "input_type": input_type,
            "truncate": "END"
        }
    )
    if response.status_code != 200:
        raise Exception(f"Cohere API error: {response.text}")
    return response.json()["embeddings"]


def chunk_text(text, filename, chunk_size=300):
    words = text.split()
    chunks = []
    step = chunk_size - 30

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append({
                "file_path": filename,
                "content": chunk
            })
    return chunks


def embed_and_store_github(workspace_id, guide_id, repo_url):
    parts = repo_url.rstrip("/").split("/")
    owner, repo = parts[-2], parts[-1]
    if repo.endswith(".git"):
        repo = repo[:-4]

    headers = {"Accept": "application/vnd.github.v3+json"}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    tree_resp = requests.get(tree_url, headers=headers)
    if tree_resp.status_code != 200:
        return False

    tree = tree_resp.json().get("tree", [])
    embeddable = [f for f in tree if f["type"] == "blob" and should_embed(f["path"])][:20]

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
    file_bytes = supabase.storage.from_("codebase-files").download(file_path)
    zip_file = zipfile.ZipFile(io.BytesIO(file_bytes))

    all_chunks = []
    embeddable = [f for f in zip_file.namelist() if should_embed(f)][:20]

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
    if not chunks:
        return

    batch_size = 10
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c["content"] for c in batch]

        try:
            embeddings = get_embeddings(texts, input_type="search_document")
        except Exception as e:
            print(f"Embedding error: {e}")
            continue

        rows = []
        for j, chunk in enumerate(batch):
            rows.append({
                "workspace_id": workspace_id,
                "guide_id": guide_id,
                "file_path": chunk["file_path"],
                "content": chunk["content"],
                "embedding": embeddings[j]
            })

        try:
            supabase.table("code_chunks").insert(rows).execute()
        except Exception as e:
            print(f"DB insert error: {e}")


def search_chunks(workspace_id, guide_id, question, top_k=3):
    question_embedding = get_embeddings([question], input_type="search_query")[0]

    result = supabase.rpc("match_code_chunks", {
        "query_embedding": question_embedding,
        "match_workspace_id": workspace_id,
        "match_guide_id": guide_id,
        "match_count": top_k
    }).execute()

    return result.data or []


def chat_with_codebase(workspace_id, guide_id, question, conversation_history):
    relevant_chunks = search_chunks(workspace_id, guide_id, question)

    if not relevant_chunks:
        context = "No specific code context found."
    else:
        context = "\n\n---\n\n".join([
            f"File: {chunk['file_path']}\n{chunk['content'][:500]}"
            for chunk in relevant_chunks
        ])

    system_prompt = f"""You are a helpful senior engineer who knows this codebase deeply.
Answer questions based on the actual code provided below.
Be specific, reference actual file names and code when relevant.
If the code context doesn't contain the answer, say so honestly.
Keep answers concise - 3-5 sentences max.

RELEVANT CODE CONTEXT:
{context}
"""

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history[-4:])
    messages.append({"role": "user", "content": question})

    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=512,
        temperature=0.3
    )

    return response.choices[0].message.content
