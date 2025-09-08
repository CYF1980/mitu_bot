from langchain_chroma import Chroma
from .embeddings_openai import get_embeddings
from ..config.settings import settings

_vector = None

def get_vectorstore():
    global _vector
    if _vector is None:
        _vector = Chroma(
            collection_name=settings.collection,
            embedding_function=get_embeddings(),
            persist_directory=settings.chroma_dir,
        )
    return _vector