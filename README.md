🤝 WeGPT – Collaborative LLM Chat with Shared Context
WeGPT is a collaborative chat platform powered by LLMs that allows multiple users to share and interact in the same chat session, each retaining their individual conversation history. Designed with real-time collaboration in mind, it merges RAG (Retrieval-Augmented Generation), vector databases, and cloud-native deployment.

💡 Key Features
Multi-User Collaborative Chat
Share a chat session with others and view contextual responses with complete message continuity. Each user's contributions are tracked while maintaining shared LLM context.

Persistent Chat History via VectorDB
Conversations are embedded using Sentence Transformers and stored in ChromaDB, enabling semantic retrieval of historical context during multi-turn chats.

LLM Integration via Groq API
Backend connected to Groq-powered LLMs for fast and contextually aware responses.

RAG-Powered Retrieval
When responding, the system uses top-N similarity search from ChromaDB to retrieve relevant past exchanges, enhancing continuity and accuracy.

🏗️ Architecture Overview
Frontend: Firebase-hosted UI for real-time messaging and session sharing

Backend: Built with FastAPI, handles user authentication, session sync, and API routing

Vector Storage: ChromaDB hosted on Render for persistent vector-based chat embeddings

LLM Inference: Groq API with support for switching models like LLaMA or Mistral

Retrieval Engine: SentenceTransformer-based embedding + Top-N vector similarity search

🚀 How It Works
Start a Chat
Login to the interface and initiate a new LLM chat session.

Share the Session
Generate a sharable link for others to join your session — all users can contribute and see the full conversation.

Smart Context Retrieval
Every user input is embedded and stored in ChromaDB. Before each new response, relevant past messages are retrieved using vector similarity to maintain contextual depth.

Get Rich Responses
The Groq LLM generates answers informed by both the current prompt and retrieved past context.

🧠 Tech Stack
Frontend: Firebase

Backend: FastAPI

LLMs: Groq API (supports models like LLaMA, Mistral)

VectorDB: ChromaDB

Embeddings: Sentence Transformers

Deployment: Render (ChromaDB backend)
