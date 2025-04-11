# combined_app.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb
import uuid
import requests
from services.firebase_utils import save_message
from services.groq_utils import call_groq_model

# Initialize ChromaDB and embedding model
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("chat_memory")
model = SentenceTransformer("all-MiniLM-L6-v2")

# FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat/{session_id}")
async def chat(session_id: str, request: Request):
    data = await request.json()
    user_input = data.get("message")
    user = data.get("sender", "User")

    # Save user message to Firebase
    save_message(session_id, user, user_input)

    # Retrieve context from vector DB
    context = get_context_from_vector_db(session_id, user_input)

    # Combine context with user input
    full_prompt = context + "\nUser: " + user_input if context else user_input

    # Call Groq model
    response = call_groq_model(full_prompt)

    # Save bot response to Firebase
    save_message(session_id, "GroqBot", response)

    # Add both user prompt and bot response to vector DB
    add_to_vector_db(session_id, f"User: {user_input}\nGroqBot: {response}")

    return {"response": response}

class AddVector(BaseModel):
    session_id: str
    prompt: str

class SearchVector(BaseModel):
    session_id: str
    query: str
    top_k: int = 3

@app.post("/add")
async def add_vector(data: AddVector):
    embedding = model.encode(data.prompt).tolist()
    vector_id = str(uuid.uuid4())
    collection.add(
        ids=[vector_id],
        documents=[data.prompt],
        embeddings=[embedding],
        metadatas=[{"session_id": data.session_id}]
    )
    return {"status": "added", "id": vector_id}

@app.post("/search")
async def search_vector(data: SearchVector):
    query_embedding = model.encode(data.query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=data.top_k,
        where={"session_id": data.session_id}
    )
    return {"results": results}

@app.get("/health")
def health():
    return {"status": "App running with combined vector and chat API"}

# Local utility functions for internal use (no longer API calls)
def get_context_from_vector_db(session_id: str, query: str, top_k: int = 3) -> str:
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"session_id": session_id}
    )
    documents = results.get("documents", [[]])[0]
    return "\n".join(documents)

def add_to_vector_db(session_id: str, prompt: str):
    embedding = model.encode(prompt).tolist()
    vector_id = str(uuid.uuid4())
    collection.add(
        ids=[vector_id],
        documents=[prompt],
        embeddings=[embedding],
        metadatas=[{"session_id": session_id}]
    )
