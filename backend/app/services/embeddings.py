from typing import List
from langchain_openai import OpenAIEmbeddings
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating embeddings"""
    
    def __init__(self):
        if settings.use_local_embeddings:
            logger.info("Using local embeddings (sentence-transformers)")
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.local_embedding_model
            )
        else:
            logger.info(f"Using OpenAI embeddings: {settings.embedding_model}")
            self.embeddings = OpenAIEmbeddings(
                model=settings.embedding_model,
                openai_api_key=settings.openai_api_key
            )
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents"""
        try:
            return self.embeddings.embed_documents(texts)
        except Exception as e:
            logger.error(f"Error generating document embeddings: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query"""
        try:
            return self.embeddings.embed_query(text)
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

# Global embedding service instance
embedding_service = EmbeddingService()