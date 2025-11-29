from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import logging
from app.config import settings
from app.services.vector_store import vector_store
from app.models import QueryRequest, ChatResponse, SourceDocument

logger = logging.getLogger(__name__)

class ChatService:
    """RAG-based chat service"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key
        )
        
        # RAG prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant that answers questions based on the user's personal knowledge base.

            Instructions:
            1. Answer the question using ONLY the information provided in the context below
            2. If the context doesn't contain enough information to answer the question, say so clearly
            3. Cite your sources by mentioning the document name when you use information from it
            4. Be concise but complete
            5. If you see conflicting information in different documents, mention both perspectives

            Context from user's documents:
            {context}

            Previous conversation:
            {history}
            """),
            ("human", "{question}")
        ])
    
    def format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for the prompt"""
        if not history:
            return "No previous conversation."
        
        formatted = []
        for msg in history[-5:]:  # Only use last 5 messages for context
            role = msg.get("role", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.capitalize()}: {content}")
        
        return "\n".join(formatted)
    
    def generate_response(self, request: QueryRequest) -> ChatResponse:
        """Generate a response using RAG"""
        try:
            # 1. Retrieve relevant documents
            search_results = vector_store.query(
                query_text=request.query,
                n_results=request.max_sources
            )
            
            if not search_results:
                return ChatResponse(
                    answer="I couldn't find any relevant information in your knowledge base to answer this question. Try uploading more documents or rephrasing your question.",
                    sources=[]
                )
            
            # 2. Format context from retrieved documents
            context_parts = []
            for i, result in enumerate(search_results, 1):
                filename = result['metadata']['filename']
                page = result['metadata'].get('page')
                content = result['content']
                
                page_info = f" (Page {page})" if page else ""
                context_parts.append(f"[Document {i}: {filename}{page_info}]\n{content}\n")
            
            context = "\n".join(context_parts)
            
            # 3. Format conversation history
            history = self.format_conversation_history(request.conversation_history)
            
            # 4. Generate response
            messages = self.prompt.format_messages(
                context=context,
                history=history,
                question=request.query
            )
            
            response = self.llm.invoke(messages)
            answer = response.content
            
            # 5. Format sources
            sources = [
                SourceDocument(
                    content=result['content'][:200] + "...",  # Truncate for brevity
                    filename=result['metadata']['filename'],
                    page=result['metadata'].get('page'),
                    relevance_score=result['relevance_score']
                )
                for result in search_results
            ]
            
            return ChatResponse(
                answer=answer,
                sources=sources
            )
        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise

# Global chat service instance
chat_service = ChatService()