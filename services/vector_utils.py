import requests

CHROMA_API_BASE = "http://localhost:8001"  # Or change to hosted IP/domain

def get_context_from_vector_db(session_id: str, query: str, top_k: int = 3) -> str:
    payload = {"session_id": session_id, "query": query, "top_k": top_k}
    res = requests.post(f"{CHROMA_API_BASE}/search", json=payload)
    results = res.json()
    documents = results.get("results", {}).get("documents", [[]])[0]
    return "\n".join(documents)

def add_to_vector_db(session_id: str, prompt: str):
    payload = {"session_id": session_id, "prompt": prompt}
    res = requests.post(f"{CHROMA_API_BASE}/add", json=payload)
    return res.json()
