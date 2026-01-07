# CosAI - Personal AI Knowledge Assistant
### Complete Implementation Guide

A secure, local first RAG (Retrieval Augmented Generation) Application that lets you chat with your own documents. It ingests your files (PDFs, TXT), understnads them using local AI models, and answers questions using Groq-AI

Think of it as the 'ChatGPT for your personal documents' - it only knows what you tell it, ensuring accuracy and reducing hallucinations


## Features
- 100% Free Tech Stack: Uses Groq (Free Tier) for intelligence and HuggingFace (Local) for memory
- Document Integestion: Specialised processing for PDFs and text files
- Strict RAG: The AI is instructed to only answer based on your documents. If the answer isn't in your files, it says "I don't know" rather than making things up
- Source Citations: Every answer cites the specific document used.
- Privacy Focused: Your documents and embeddings stay on your machine. Only the text is relevant to your specific query is sent to the LLM


## Tech Stack
- Backend: Python 3.12.1, FastAPI
- Frontned: React, TypeScript, Tailwind CSS, Vite
- LLM (The Brain): Groq API - llama-3.3-70b-versatile
- Embeddings (The Memory): HuggingFace running locally - sentence-transformers/all-MiniLM-L6-v2
- Vector Database: ChromaDB (Local File storage)


## Models
For Embeddings (The Memory): sentence-transformers/all-MiniLM-L6-v2
- Source: HuggingFace running locally
- Role: Processes your PDFs and text files to create "memory" stored on your machine.
- Privacy: Ensures your full documents and embeddings stay on your device.

For LLM (The Brain): Groq API - llama-3.3-70b-versatile
- Source: Groq (Free Tier)
- Role: Handles the intelligence and text generation.
- Performance: High-speed inference using the versatile Llama 3.3 70B model.

For Storage: ChromaDB
- Type: Local File Storage
- Role: Acts as the Vector Database to store your document embeddings efficiently.

Hybrid Approach (Groq + Local HuggingFace)


## Verdict
It is working exactly as designed.

You might be thinking, "Wait, I thought AI was smart? Why doesn't it know Paris is the capital of France?"

The Reason: You built a RAG (Retrieval-Augmented Generation) application.

Standard ChatGPT: Uses its own memory of the internet to answer anything.

Your App: Is specifically programmed to ignore its own memory and only use the documents you give it.


## Project Structure
```
ai-review/
├── backend/
│   ├── app/
│   │   ├── main.py                 # Server entry point & Telemetry fix
│   │   ├── config.py               # Env variable management
│   │   ├── services/
│   │   │   ├── chat_service.py     # Groq LLM logic
│   │   │   ├── embeddings.py       # Local HuggingFace embeddings
│   │   │   └── vector_store.py     # ChromaDB management
│   ├── data/                       # Stores your uploaded files & DB (GitIgnored)
│   ├── .env                        # API Keys (GitIgnored)
│   └── venv/                       # Python Virtual Environment
│
└── frontend/
    ├── src/                        # React Source Code
    └── package.json                # JS Dependencies
```

## Installation & Setup

Prerequistes
1. Python 3.12.1 installed
2. Node.js & npm installed
3. Groq API Key (Get one for free at console.groq.com)



### 1. Backend Setup
Open terminal and navigate to the backend:
`cd backend`

Create and Activate Virtual Environment:
```
# Mac/Linux
python3.12 -m venv venv
source venv/bin/activate

# Windows
py -3.12 -m venv venv
venv\Scripts\activate


# To deactivate for whatever reason
rm -rf venv
```

Install dependencies:

```
pip install langchain langchain-community langchain-groq langchain-huggingface sentence-transformers python-dotenv langchain-text-splitters uvicorn fastapi watchfiles
```
Note: This installs the specific modern libaries required for Python 3.12 compatibility

Configure Environment:
1. Create a file named `.env` in the `backend/` folder
2. Add your API key and telemetry setting to prevent database errors
```
GROQ_API_KEY=gsk_your_actual_key_here
ANONYMIZED_TELEMETRY=False
```

Start the Server:
`python -m app.main`

You should see `Uvicorn running on http://0.0.0.0:8000`


### 2. Frontend Setup
Open a new terminal window, keep the backend running, and navigate to the frontend: `cd frontend`

Install Dependencies: `npm install`

Start the App: `npm run dev`

The app should open at `http://localhost:5173` (or port 3000)