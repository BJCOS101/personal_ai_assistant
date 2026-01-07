### Personal AI Knowledge Assistant - Complete Implementation Guide


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






### CosAI - Personal AI Knowledge Assistant

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