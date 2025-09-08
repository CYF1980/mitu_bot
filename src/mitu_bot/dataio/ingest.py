# src/mitu_bot/dataio/ingest.py
from langchain_chroma import Chroma
from langchain_core.documents import Document
import csv, os
from .loaders import csv_to_documents
from ..adapters.embeddings_openai import get_embeddings
from ..config.settings import settings

def ingest_csv_to_chroma(path: str, rebuild: bool = False) -> int:
    """Load a CSV into Documents, write to Chroma, and return doc count."""
    docs = csv_to_documents(path)
    build_vectorstore(docs, rebuild=rebuild)
    return len(docs)

def build_vectorstore(docs: list[Document], rebuild: bool = False):
    if rebuild and os.path.exists(settings.chroma_dir):
        import shutil; shutil.rmtree(settings.chroma_dir)
    vs = Chroma(collection_name=settings.collection,
                embedding_function=get_embeddings(),
                persist_directory=settings.chroma_dir)
    vs.add_documents(docs)
    return vs
