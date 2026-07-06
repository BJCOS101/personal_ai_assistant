from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os
from datetime import datetime
from app.config import settings
from app.models import (
    QueryRequest,
    ChatResponse,
    DocumentUploadResponse,
    DocumentListResponse,
    DocumentMetadata,
    LLMProviderStatus,
    LLMProviderUpdateRequest,
)
from app.services.document_processor import document_processor
from app.services.vector_store import vector_store
from app.services.chat_service import chat_service, is_ollama_running
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document"""
    try:
        # Strip any directory components from the uploaded filename
        # (e.g. "../../etc/passwd" -> "passwd") so a crafted filename
        # can never write outside the documents directory.
        safe_filename = os.path.basename(file.filename or "")
        if not safe_filename or safe_filename in (".", ".."):
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md']
        file_extension = os.path.splitext(safe_filename)[1].lower()

        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
            )

        file_path = os.path.join(settings.documents_directory, safe_filename)

        # Belt-and-braces check: confirm the final path is really inside
        # the documents directory before we write anything to disk.
        documents_dir = os.path.abspath(settings.documents_directory)
        if not os.path.abspath(file_path).startswith(documents_dir + os.sep):
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Save file, rejecting it partway through if it exceeds the size limit
        max_bytes = settings.max_upload_size_mb * 1024 * 1024
        bytes_written = 0
        with open(file_path, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                bytes_written += len(chunk)
                if bytes_written > max_bytes:
                    buffer.close()
                    os.remove(file_path)
                    raise HTTPException(
                        status_code=413,
                        detail=f"File exceeds max upload size of {settings.max_upload_size_mb}MB"
                    )
                buffer.write(chunk)

        # Process document
        chunks = document_processor.process_document(file_path)
        
        # Add to vector store
        num_chunks = vector_store.add_documents(chunks)
        
        return DocumentUploadResponse(
            success=True,
            filename=safe_filename,
            num_chunks=num_chunks,
            message=f"Successfully processed {safe_filename} into {num_chunks} chunks"
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

@router.get("/llm-provider", response_model=LLMProviderStatus)
async def get_llm_provider():
    """Report which 'answer writer' (LLM) is currently active, and what's available."""
    return LLMProviderStatus(
        provider=settings.llm_provider,
        offline_mode=(settings.llm_provider == "ollama"),
        groq_configured=bool(settings.groq_api_key),
        ollama_running=is_ollama_running(),
    )

@router.post("/llm-provider", response_model=LLMProviderStatus)
async def set_llm_provider(request: LLMProviderUpdateRequest):
    """Flip between offline (Ollama) and online (Groq) mode. Takes effect immediately."""
    wants_offline = request.offline_mode

    if wants_offline:
        if not is_ollama_running():
            raise HTTPException(
                status_code=503,
                detail=(
                    "Ollama isn't running. Start it with: brew services start ollama "
                    "(or 'ollama serve' in a terminal), then try again."
                )
            )
        settings.llm_provider = "ollama"
    else:
        if not settings.groq_api_key:
            raise HTTPException(
                status_code=400,
                detail="Cannot switch to online mode: no GROQ_API_KEY is configured in .env"
            )
        settings.llm_provider = "groq"

    logger.info(f"LLM provider switched to: {settings.llm_provider}")

    return LLMProviderStatus(
        provider=settings.llm_provider,
        offline_mode=(settings.llm_provider == "ollama"),
        groq_configured=bool(settings.groq_api_key),
        ollama_running=is_ollama_running(),
    )

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "document_count": vector_store.collection.count()
    }