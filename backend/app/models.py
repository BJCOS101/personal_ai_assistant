from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class DocumentMetadata(BaseModel):
    filename: str
    file_path: str
    file_type: str
    file_size: int
    upload_date: datetime
    num_chunks: int

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="The question to ask")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=[],
        description="Previous conversation messages"
    )
    max_sources: int = Field(default=3, ge=1, le=10, description="Max source documents to retrieve")

class SourceDocument(BaseModel):
    content: str
    filename: str
    page: Optional[int] = None
    relevance_score: float

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
    conversation_id: Optional[str] = None

class DocumentUploadResponse(BaseModel):
    success: bool
    filename: str
    num_chunks: int
    message: str

class DocumentListResponse(BaseModel):
    documents: List[DocumentMetadata]
    total_count: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None