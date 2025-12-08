import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import fitz  # PyMuPDF              Need to comment out for time being due to build issues
from langchain_community.document_loaders import PyPDFLoader
from docx import Document as DocxDocument
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import settings

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handle document ingestion and text extraction"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def extract_text_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from PDF with page numbers"""
        try:
            doc = fitz.open(file_path)
            pages_content = []
            
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                if text.strip():
                    pages_content.append({
                        "page": page_num,
                        "content": text
                    })
            
            doc.close()
            return pages_content
        except Exception as e:
            logger.error(f"Error extracting PDF text from {file_path}: {e}")
            raise
    
    def extract_text_from_docx(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from DOCX file"""
        try:
            doc = DocxDocument(file_path)
            full_text = []
            for para in doc.paragraphs:
                if para.text.strip():
                    full_text.append(para.text)
            
            content = "\n\n".join(full_text)
            return [{"page": None, "content": content}]
        except Exception as e:
            logger.error(f"Error extracting DOCX text from {file_path}: {e}")
            raise
    
    def extract_text_from_txt(self, file_path: str) -> List[Dict[str, Any]]:
        """Extract text from TXT/MD files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [{"page": None, "content": content}]
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise
    
    def process_document(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Process a document and return chunks with metadata
        
        Returns:
            List of dicts with keys: content, metadata (filename, page, chunk_id)
        """
        filename = os.path.basename(file_path)
        file_extension = Path(file_path).suffix.lower()
        
        # Extract text based on file type

        # uncomment below for time being due to build issues, comment when working
        # if file_extension == '.pdf':
        #     raise ValueError("PDF support temporarily disabled. Use TXT, MD, or DOCX instead.")
        # elif file_extension in ['.docx', '.doc']:
        #     pages_content = self.extract_text_from_docx(file_path)

        # comment below for time being due to build issues, uncomment when working
        if file_extension == '.pdf':
            pages_content = self.extract_text_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            pages_content = self.extract_text_from_docx(file_path)


        elif file_extension in ['.txt', '.md']:
            pages_content = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        # Split into chunks and add metadata
        chunks = []
        chunk_id = 0
        
        for page_data in pages_content:
            page_num = page_data.get("page")
            content = page_data["content"]
            
            # Split content into chunks
            text_chunks = self.text_splitter.split_text(content)
            
            for chunk_text in text_chunks:
                chunks.append({
                    "content": chunk_text,
                    "metadata": {
                        "filename": filename,
                        "file_path": file_path,
                        "page": page_num,
                        "chunk_id": chunk_id
                    }
                })
                chunk_id += 1
        
        logger.info(f"Processed {filename}: {len(chunks)} chunks created")
        return chunks

# Global document processor instance
document_processor = DocumentProcessor()