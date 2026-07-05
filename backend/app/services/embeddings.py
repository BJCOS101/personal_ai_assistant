from langchain_huggingface import HuggingFaceEmbeddings
from app.config import settings

# This uses a free, LOCAL model to turn text into numbers ("embeddings").
# It runs on your computer, so no API key or internet is needed for this part.
# The exact model name comes from config.py (single source of truth).
embedding_service = HuggingFaceEmbeddings(
    model_name=settings.embedding_model,
    # Rescale every embedding to length 1 ("normalize") so that our
    # cosine (angle-based) similarity scores are clean and consistent.
    encode_kwargs={"normalize_embeddings": True},
)
