from langchain_openai import ChatOpenAI
from ..config.settings import settings

def get_llm():
    return ChatOpenAI(
        model=settings.llm_model,
        temperature=0.3,
        timeout=30,
        max_tokens=None,
    )
