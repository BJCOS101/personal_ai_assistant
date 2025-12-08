from langchain_huggingface import HuggingFaceEmbeddings

# This uses a free, local model to turn text into numbers (Embeddings)
# It runs on your computer, so no API key is needed for this part.
embedding_service = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)