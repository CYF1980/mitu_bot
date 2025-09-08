from langchain_openai import OpenAIEmbeddings
from ..config.settings import settings

def get_embeddings():
    return OpenAIEmbeddings(model=settings.embed_model)
