### Personal AI Knowledge Assistant - Complete Implementation Guide


Component Responsibilities
Backend Components:

main.py: FastAPI app initialization, CORS, middleware
config.py: Environment variables, API keys, paths
models.py: Request/response schemas (QueryRequest, ChatResponse, etc.)
document_processor.py: Extract text from PDFs/DOCX, split into chunks
vector_store.py: ChromaDB operations (add, query, delete)
chat_service.py: RAG pipeline, LLM prompting, source citation
embeddings.py: Generate embeddings (OpenAI or local)
routes.py: REST endpoints for document management
websocket.py: Real-time chat via WebSocket

Frontend Components:

ChatInterface.tsx: Main chat UI with message history
DocumentUpload.tsx: Upload and ingest new documents
Message.tsx: Render individual messages with citations
Sidebar.tsx: Show ingested documents, manage collection
api.ts: Axios client for backend communication



Commands:

cd frontend
npm run dev

to restart frontend: (Ctrl + C)


cd backend
source venv/bin/activate
python -m app.main

to restart backend: (Ctrl + C) or deactivate


ill make a script for everything eventually



need to use virtual environemnet for backend, use python 3.12

deactivate
rm -rf venv

python3.11 --version
# OR
python3.12 --version
# OR
python3.10 --version


# Use the specific python version to create the venv
python3.11 -m venv venv

# Activate the new environment
source venv/bin/activate

pip install -r requirements.txt

python -m app.main




Using Free AI Models - Complete Integration Guide
Great choice! Let's replace OpenAI with free, open-source models that run locally. For your use case (searching and analyzing documents), I'll guide you through the best options.
Best Free Model Options for Your Project
Recommended Setup (Best Balance)
For Embeddings: sentence-transformers/all-MiniLM-L6-v2

Fast, lightweight (80MB)
Good semantic search quality
Runs on CPU efficiently

For LLM (Text Generation): Choose one based on your hardware:

Mistral-7B-Instruct (Recommended - Best Quality)

7B parameters
Excellent instruction following
Requires ~8GB RAM (or 4GB VRAM for GPU)
Via Hugging Face Transformers or Ollama


Phi-3-mini (Lightweight Alternative)

3.8B parameters
Good quality, very fast
Requires ~4GB RAM
Great for laptops/lower-end hardware


LLaMA 3.2 3B (Latest from Meta)

3B parameters
State-of-the-art for its size
Requires ~4GB RAM



My Recommendation: Ollama + Mistral 7B
Why Ollama?

Easiest setup (one command)
Automatic model management
Optimized inference
Works on CPU and GPU
Simple API (OpenAI-compatible)






Verdict: It is working exactly as designed.

You might be thinking, "Wait, I thought AI was smart? Why doesn't it know Paris is the capital of France?"

The Reason: You built a RAG (Retrieval-Augmented Generation) application.

Standard ChatGPT: Uses its own memory of the internet to answer anything.

Your App: Is specifically programmed to ignore its own memory and only use the documents you give it.









Here is the consolidated setup guide for your README.md.

Since you have already modified the code files (main.py, chat_service.py, etc.) to use Groq and local embeddings, a new user simply needs to install the correct libraries and add their keys.

You can copy-paste the sections below directly into your README.

🛠️ Installation & Setup
Prerequisites
Python 3.10+

Node.js & npm

Groq API Key (Get one for free at console.groq.com)

1. Backend Setup (The Brain)
Navigate to the backend folder:

Bash

cd backend
Create and Activate a Virtual Environment:

Bash

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
Install Dependencies: These are the specific libraries needed for Groq and Local Embeddings:

Bash

pip install langchain langchain-community langchain-groq langchain-huggingface sentence-transformers python-dotenv langchain-text-splitters uvicorn fastapi
Configure Environment Variables:

Create a file named .env in the backend folder.

Add your Groq API key and the telemetry setting:

Code snippet

GROQ_API_KEY=gsk_your_actual_key_here
ANONYMIZED_TELEMETRY=False
Start the Server:

Bash

python -m app.main
The server should start at http://localhost:8000.

2. Frontend Setup (The Interface)
Open a new terminal and navigate to the frontend folder:

Bash

cd frontend
Install Dependencies:

Bash

npm install
Start the Application:

Bash

npm start
The application should open at http://localhost:3000.

3. Usage Guide
Open the web interface (http://localhost:3000).

Upload a Document: Drag and drop a PDF or TXT file (e.g., notes.txt) to the sidebar.

Note: Since this uses RAG, the bot will NOT answer questions until you give it a document to read.

Ask a Question: Type a question related to the document you just uploaded.

💡 Troubleshooting
"Capture() takes 1 positional argument...": Ensure ANONYMIZED_TELEMETRY=False is in your .env file and that you have restarted the backend.

ModuleNotFound Errors: Ensure you activated the virtual environment (source venv/bin/activate) before running the server.



CosAI - Personal AI Knowledge Assistant

A secure, local first RAG (Retrieval Augmented Generation) Application that lets you chat with your own documents. It ingests your files (PDFs, TXT), understnads them using local AI models, and answers questions using Groq-AI

Think of it as the 'ChatGPT for your personal documents' - it only knows what you tell it, ensuring accuracy and reducing hallucinations


Features
- 100% Free Tech Stack: Uses Groq (Free Tier) for intelligence and HuggingFace (Local) for memory
- Document Integestion: Specialised processing for PDFs and text files
- Strict RAG: The AI is instructed to only answer based on your documents. If the answer isn't in your files, it says "I don't know" rather than making things up
- Source Citations: Every answer cites the specific document used.
- Privacy Focused: Your documents and embeddings stay on your machine. Only the text is relevant to your specific query is sent to the LLM


Tech Stack
- Backend: Python 3.12.1, FastAPI
- Frontned: React, TypeScript, Tailwind CSS, Vite
- LLM (The Brain): Groq API - llama-3.3-70b-versatile
- Embeddings (The Memory): HuggingFace running locally - sentence-transformers/all-MiniLM-L6-v2
- Vector Database: ChromaDB (Local File storage)


Project Structure
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

Installation & Setup

Prerequistes
1. Python 3.12.1 installed
2. Node.js & npm installed
3. Groq API Key (Get one for free at console.groq.com)


1. Backend Setup
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
```

Install dependencies:
Note: This installs the specific modern libaries required for Python 3.12 compatibility
`pip install langchain langchain-community langchain-groq langchain-huggingface sentence-transformers python-dotenv langchain-text-splitters uvicorn fastapi watchfiles`

Configure Environment:
1. Create a file named `.env` in the `backend/` folder
2. Add your API key and telemetry setting to prevent database errors
```
GROQ_API_KEY=gsk_your_actual_key_here
ANONYMIZED_TELEMETRY=False
```

Start the Server:
`python -m app.main`
You should see 'Uvicorn running on http://0.0.0.0:8000'


2. Frontend Setup
Open a new terminal window, keep the backend running, and navigate to the frontend:
`cd frontend`

Install Dependencies:
`npm install`

Start the App:
`npm run dev`
The app should open at `http://localhost:5173` (or port 3000)