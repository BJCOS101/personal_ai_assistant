from typing import List, Dict, Any
import requests
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

import logging
from app.config import settings
from app.services.vector_store import vector_store
from app.models import QueryRequest, ChatResponse, SourceDocument

logger = logging.getLogger(__name__)


def is_ollama_running() -> bool:
    """Ping the local Ollama server to see if it's actually up."""
    try:
        resp = requests.get(f"{settings.ollama_base_url}/api/tags", timeout=1.5)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def build_llm(provider: str):
    """
    Build the "answer writer" model for a given provider name.

      - "groq"   -> cloud model (fast, high quality, sends retrieved
                     text to Groq's servers over the internet)
      - "ollama" -> local model running on this machine via Ollama
                     (fully offline, nothing leaves your computer)
    """
    if provider == "ollama":
        logger.info(f"Using LOCAL/offline LLM via Ollama: {settings.ollama_model}")
        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.llm_temperature,
            num_predict=settings.max_tokens,
        )

    if provider == "groq":
        if not settings.groq_api_key:
            raise ValueError(
                "GROQ_API_KEY is required when LLM_PROVIDER=groq. "
                "Either set it in .env, or switch to offline mode."
            )
        logger.info(f"Using CLOUD LLM via Groq: {settings.llm_model}")
        return ChatGroq(
            api_key=settings.groq_api_key,
            model_name=settings.llm_model,
            temperature=settings.llm_temperature,
            max_tokens=settings.max_tokens,
        )

    raise ValueError(f"Unknown llm_provider: {provider!r}")


class ChatService:
    """RAG-based chat service"""

    def __init__(self):
        # One LLM "client" object per provider, built lazily and reused.
        # Switching providers at runtime (the UI toggle) just changes which
        # cached client we read from settings.llm_provider each request.
        self._llm_cache: Dict[str, Any] = {}
        self._get_llm()  # build the startup default now, so config errors surface immediately

        # RAG prompt template (Keep the rest the same)
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
    
    def _get_llm(self):
        """Return the LLM client for whichever provider is currently active,
        building it once and reusing it after that."""
        provider = settings.llm_provider
        if provider not in self._llm_cache:
            self._llm_cache[provider] = build_llm(provider)
        return self._llm_cache[provider]

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
            
            response = self._get_llm().invoke(messages)
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