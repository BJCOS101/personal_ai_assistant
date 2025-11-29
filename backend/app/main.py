from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import routes, websocket
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Personal AI Knowledge Assistant",
    description="Query your personal documents with AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api", tags=["documents"])
app.include_router(websocket.router, prefix="/api", tags=["websocket"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting Personal AI Knowledge Assistant")
    logger.info(f"Document directory: {settings.documents_directory}")
    logger.info(f"ChromaDB directory: {settings.chroma_persist_directory}")
    logger.info(f"Using {'local' if settings.use_local_embeddings else 'OpenAI'} embeddings")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Personal AI Knowledge Assistant")

@app.get("/")
async def root():
    return {
        "message": "Personal AI Knowledge Assistant API",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )