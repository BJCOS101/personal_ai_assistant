from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os


class Settings(BaseSettings):
    """
    Single source of truth for all app settings.

    Values are read from the .env file (or real environment variables).
    Anything not provided falls back to the default written here.
    """

    # --- API keys ---
    # Optional because it's only needed when llm_provider = "groq".
    # Fully-offline (llm_provider = "ollama") mode needs no API key at all.
    groq_api_key: Optional[str] = None

    # --- LLM: the "answer writer" ---
    # "groq"   -> cloud, fast, high quality, sends retrieved text to Groq's servers
    # "ollama" -> fully local/offline, nothing ever leaves this machine
    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"          # used when llm_provider = "groq"
    ollama_model: str = "llama3.1:8b"                    # used when llm_provider = "ollama"
    ollama_base_url: str = "http://localhost:11434"      # Ollama's local server address
    llm_temperature: float = 0.0   # 0 = stay factual / grounded; higher = more creative
    max_tokens: int = 1000         # rough cap on answer length

    # --- Embeddings: the LOCAL "text -> meaning numbers" model ---
    # Runs on your machine. No API key, no internet needed for this step.
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # --- Vector database: local storage of the embeddings ---
    chroma_persist_directory: str = "./data/chroma_db"
    chroma_collection_name: str = "personal_knowledge"
    anonymized_telemetry: bool = False

    # --- Document ingestion ---
    documents_directory: str = "./data/documents"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_upload_size_mb: int = 20  # reject uploads bigger than this

    # --- Retrieval quality ---
    # Chunks scoring below this similarity (0.0 - 1.0) are treated as "not
    # relevant enough" and thrown away before reaching the AI.
    # Lower it if the app too often says "I couldn't find anything";
    # raise it if answers use weak/off-topic sources.
    relevance_threshold: float = 0.3

    # --- Web server ---
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Ignore any extra keys in .env (e.g. LLM_PROVIDER, USE_LOCAL_EMBEDDINGS)
        # instead of crashing on startup. Keeps old .env files working.
        extra="ignore",
    )


# Global settings instance
settings = Settings()

# Create necessary directories on startup
os.makedirs(settings.documents_directory, exist_ok=True)
os.makedirs(settings.chroma_persist_directory, exist_ok=True)
