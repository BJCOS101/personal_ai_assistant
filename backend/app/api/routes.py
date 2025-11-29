from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
import shutil
from datetime import datetime
from app.config import settings
from app.models import (
    QueryRequest,
    ChatResponse,
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentMetadata
)
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store
from app.services.chat_service import chat_service
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )
        
        # Save file
        file_path = os.path.join(settings.documents_directory, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process document
        chunks = document_processor.process_document(file_path)
        
        # Add to vector store
        num_chunks = vector_store.add_documents(chunks)
        
        return DocumentUploadResponse(
            success=True,
            filename=file.filename,
            num_chunks=num_chunks,
            message=f"Successfully processed {file.filename} into {num_chunks} chunks"
        )
    
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=ChatResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base"""
    try:
        response = chat_service.generate_response(request)
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents", response_model=DocumentListResponse)
async def list_documents():
    """List all documents in the knowledge base"""
    try:
        documents = vector_store.list_documents()
        
        # Add file metadata
        document_list = []
        for doc in documents:
            file_path = doc['file_path']
            if os.path.exists(file_path):
                file_stats = os.stat(file_path)
                document_list.append(
                    DocumentMetadata(
                        filename=doc['filename'],
                        file_path=file_path,
                        file_type=os.path.splitext(doc['filename'])[1],
                        file_size=file_stats.st_size,
                        upload_date=datetime.fromtimestamp(file_stats.st_mtime),
                        num_chunks=doc['num_chunks']
                    )
                )
        
        return DocumentListResponse(
            documents=document_list,
            total_count=len(document_list)
        )
    
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document from the knowledge base"""
    try:
        # Delete from vector store
        num_deleted = vector_store.delete_document(filename)
        
        # Delete physical file
        file_path = os.path.join(settings.documents_directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return {
            "success": True,
            "message": f"Deleted {filename} ({num_deleted} chunks removed)"
        }
    
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear")
async def clear_knowledge_base():
    """Clear all documents from the knowledge base"""
    try:
        vector_store.clear_collection()
        
        # Clear documents directory
        for filename in os.listdir(settings.documents_directory):
            file_path = os.path.join(settings.documents_directory, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return {"success": True, "message": "Knowledge base cleared"}
    
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "document_count": vector_store.collection.count()
    }