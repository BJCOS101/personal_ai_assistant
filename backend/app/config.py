from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # API Keys
    groq_api_key: str
    llm_provider: str = "groq"
    
    # Embedding settings
    use_local_embeddings: bool = False
    embedding_model: str = "text-embedding-3-small"
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Database settings
    chroma_persist_directory: str = "./data/chroma_db"
    chroma_collection_name: str = "personal_knowledge"

    anonymized_telemetry: bool = False
    
    # Document settings
    documents_directory: str = "./data/documents"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # LLM settings
    # CHANGED: Default to a Groq-supported model (Llama 3 70B is a good balance)
    llm_model: str = "llama3-70b-8192" 
    llm_temperature: float = 0.0
    max_tokens: int = 1000
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

# Global settings instance
settings = Settings()

# Create necessary directories
os.makedirs(settings.documents_directory, exist_ok=True)
os.makedirs(settings.chroma_persist_directory, exist_ok=True)