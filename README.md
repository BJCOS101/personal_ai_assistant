# CosAI - Personal AI Knowledge Assistant
### Complete Implementation Guide

A secure, local-first RAG (Retrieval-Augmented Generation) application that lets you chat with your own documents. It ingests your files (PDF, DOCX, TXT, MD), understands them using a local embedding model, and answers questions using an LLM of your choice - either a fast cloud model (Groq) or a fully offline local model (Ollama).

Think of it as the "ChatGPT for your personal documents" - it only knows what you tell it, ensuring accuracy and reducing hallucinations.


## Features
- **Document Ingestion**: Specialized processing for PDF, DOCX, TXT, and MD files
- **Strict RAG**: The AI is instructed to only answer based on your documents. If the answer isn't in your files, it says "I don't know" rather than making things up
- **Relevance Filtering**: Retrieved passages that aren't actually similar enough to your question are dropped before ever reaching the AI, instead of being fed in blindly
- **Source Citations**: Every answer cites the specific document (and page, for PDFs) it came from
- **Online / Offline Toggle**: Switch between a cloud LLM (Groq - fast, free tier) and a fully local LLM (Ollama - nothing leaves your machine) with one click in the UI, no restart required
- **Privacy Focused**: Your documents and embeddings always stay on your machine. In online mode, only the small text snippets relevant to your specific query are sent to the cloud LLM; in offline mode, nothing is sent anywhere
- **Upload Safety**: Uploaded filenames are sanitized and file size is capped (default 20MB) before anything is written to disk


## Tech Stack
- Backend: Python 3.12, FastAPI
- Frontend: React, TypeScript, Tailwind CSS, Vite
- LLM (The Brain) - choose one, switchable live in the UI:
  - **Groq API** (cloud) - `llama-3.3-70b-versatile`
  - **Ollama** (local/offline) - `llama3.1:8b`
- Embeddings (The Memory): HuggingFace `sentence-transformers/all-MiniLM-L6-v2`, always run locally
- Vector Database: ChromaDB (local file storage, cosine similarity)


## Models

**Embeddings (The Memory)** - `sentence-transformers/all-MiniLM-L6-v2`
- Source: HuggingFace, runs locally
- Role: Turns your document text into "meaning coordinates" (embeddings) so relevant passages can be found later
- Privacy: Runs on your machine - no API key, no internet required for this step

**LLM (The Brain)** - two interchangeable options:
| | Groq (online) | Ollama (offline) |
|---|---|---|
| Model | llama-3.3-70b-versatile | llama3.1:8b |
| Where it runs | Groq's cloud servers | Your own computer |
| Needs internet | Yes | No |
| Speed | Very fast | Slower (depends on your hardware) |
| Answer quality | Higher (70B model) | Good (8B model) |
| Privacy | Retrieved snippets sent to Groq | Nothing leaves your machine |

Switch between them anytime with the **Offline Mode** toggle in the app header - it takes effect immediately, no restart needed.

**Storage** - ChromaDB
- Type: Local file storage (`backend/data/chroma_db`)
- Role: Stores your document embeddings and finds the closest matches to a question using cosine similarity


## Verdict

You might be thinking, "Wait, I thought AI was smart? Why doesn't it know Paris is the capital of France?"

The Reason: You built a RAG (Retrieval-Augmented Generation) application.

Standard ChatGPT: Uses its own memory of the internet to answer anything.

Your App: Is specifically instructed to ignore its own memory and only use the documents you give it.


## Project Structure
```
personal_ai_assistant/
├── backend/
│   ├── app/
│   │   ├── main.py                    # Server entry point & startup/shutdown logic
│   │   ├── config.py                  # Single source of truth for all settings (reads .env)
│   │   ├── models.py                  # Request/response data shapes
│   │   ├── api/
│   │   │   ├── routes.py              # Upload, query, document list, LLM provider toggle
│   │   │   └── websocket.py           # Real-time chat over WebSocket
│   │   └── services/
│   │       ├── chat_service.py        # RAG logic + Groq/Ollama switching
│   │       ├── embeddings.py          # Local HuggingFace embeddings
│   │       ├── document_processor.py  # Text extraction + chunking
│   │       └── vector_store.py        # ChromaDB management
│   ├── data/                          # Stores your uploaded files & DB (gitignored)
│   ├── .env                           # Your local settings & API key (gitignored)
│   ├── .env.example                   # Template showing every available setting
│   ├── requirements.txt               # Exact Python dependencies
│   └── venv/                          # Python virtual environment
│
└── frontend/
    ├── src/
    │   ├── app.tsx                    # App shell + header (includes the offline toggle)
    │   ├── components/                # ChatInterface, DocumentUpload, Sidebar, OfflineModeToggle
    │   ├── services/api.ts            # All calls to the backend API
    │   └── types/index.ts             # Shared TypeScript types
    └── package.json                   # JS dependencies
```


## Installation & Setup

### Prerequisites
1. Python 3.12 installed
2. Node.js & npm installed
3. **For online mode**: a free Groq API key from [console.groq.com](https://console.groq.com)
4. **For offline mode** (optional): [Ollama](https://ollama.com) installed locally

You don't need both - pick whichever mode(s) you want to use. You can always add the other later; switching is just a setting.


### 1. Backend Setup

Open a terminal and navigate to the backend:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
# Mac/Linux
python3.12 -m venv venv
source venv/bin/activate

# Windows
py -3.12 -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Configure your environment:
1. Copy the template: `cp .env.example .env`
2. Open `backend/.env` and fill in your values. At minimum, for online mode:
```
GROQ_API_KEY=gsk_your_actual_key_here
LLM_PROVIDER=groq
```
For offline-only mode, you can instead set `LLM_PROVIDER=ollama` and leave `GROQ_API_KEY` blank (see step 3 below).

Start the server:
```bash
python -m app.main
```
You should see `Uvicorn running on http://0.0.0.0:8000` with no errors.


### 2. Frontend Setup

Open a **new** terminal window, keep the backend running, and navigate to the frontend:
```bash
cd frontend
npm install
npm run dev
```
The app should open at `http://localhost:5173`.


### 3. (Optional) Offline Mode via Ollama

If you want to run entirely offline - no internet, no API key, nothing leaves your machine - install Ollama and pull a model once:

```bash
# Install Ollama (Mac, via Homebrew)
brew install ollama

# Start Ollama as a background service (auto-starts on login)
brew services start ollama

# Download the model (one-time, ~4.7GB)
ollama pull llama3.1:8b
```

Once that's done, you can switch to offline mode two ways:
- **In the UI**: click the "Offline Mode" toggle in the app header - takes effect immediately
- **In `.env`**: set `LLM_PROVIDER=ollama` and restart the backend

Requires roughly 16GB of RAM for comfortable performance on Apple Silicon.


## Usage

1. Upload a document (PDF, DOCX, TXT, or MD) via the sidebar
2. Ask a question about it in the chat box
3. Toggle **Offline Mode** in the header anytime to switch between the cloud LLM (Groq) and the fully local LLM (Ollama) - no restart needed
4. Every answer shows which document(s) it came from
