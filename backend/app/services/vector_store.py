import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import logging
from app.config import settings
from app.services.embeddings import embedding_service

logger = logging.getLogger(__name__)

class VectorStore:
    """ChromaDB vector store wrapper"""
    
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={"description": "Personal knowledge base"}
        )
        
        logger.info(f"ChromaDB initialized. Collection: {settings.chroma_collection_name}")
        logger.info(f"Current document count: {self.collection.count()}")
    
    def add_documents(self, chunks: List[Dict[str, Any]]) -> int:
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of dicts with 'content' and 'metadata' keys
        
        Returns:
            Number of chunks added
        """
        if not chunks:
            return 0
        
        try:
            # Prepare data for ChromaDB
            documents = [chunk["content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            ids = [
                f"{chunk['metadata']['filename']}_chunk_{chunk['metadata']['chunk_id']}"
                for chunk in chunks
            ]
            
            # Generate embeddings
            embeddings = embedding_service.embed_documents(documents)
            
            # Add to collection
            self.collection.add(
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(chunks)} chunks to vector store")
            return len(chunks)
        
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {e}")
            raise
    
    def query(
        self,
        query_text: str,
        n_results: int = 3,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Query the vector store
        
        Returns:
            List of dicts with keys: content, metadata, relevance_score
        """
        try:
            # Generate query embedding
            query_embedding = embedding_service.embed_query(query_text)
            
            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    formatted_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "relevance_score": 1 - results['distances'][0][i]  # Convert distance to similarity
                    })
            
            return formatted_results
        
        except Exception as e:
            logger.error(f"Error querying vector store: {e}")
            raise
    
    def delete_document(self, filename: str) -> int:
        """Delete all chunks from a specific document"""
        try:
            # Get all IDs for this filename
            results = self.collection.get(
                where={"filename": filename}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} chunks for {filename}")
                return len(results['ids'])
            
            return 0
        
        except Exception as e:
            logger.error(f"Error deleting document {filename}: {e}")
            raise
    
    def list_documents(self) -> List[Dict[str, Any]]:
        """List all unique documents in the vector store"""
        try:
            results = self.collection.get()
            
            # Group by filename
            documents = {}
            for metadata in results['metadatas']:
                filename = metadata['filename']
                if filename not in documents:
                    documents[filename] = {
                        "filename": filename,
                        "file_path": metadata.get('file_path', ''),
                        "num_chunks": 0
                    }
                documents[filename]['num_chunks'] += 1
            
            return list(documents.values())
        
        except Exception as e:
            logger.error(f"Error listing documents: {e}")
            raise
    
    def clear_collection(self):
        """Clear all documents from the collection"""
        try:
            self.client.delete_collection(settings.chroma_collection_name)
            self.collection = self.client.create_collection(
                name=settings.chroma_collection_name,
                metadata={"description": "Personal knowledge base"}
            )
            logger.info("Cleared vector store collection")
        except Exception as e:
            logger.error(f"Error clearing collection: {e}")
            raise

# Global vector store instance
vector_store = VectorStore()