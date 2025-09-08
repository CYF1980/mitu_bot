from langchain_core.documents import Document
from ..state import AgentState
from ...adapters.vectorstore_chroma import get_vectorstore
from ...adapters.embeddings_openai import get_embeddings

def retrieve_node(state: AgentState) -> AgentState:
    question = state.get("text", "")
    if not question:
        state["context"] = []
        return state
    vs = get_vectorstore()
    embeddings = get_embeddings()
    docs: list[Document] = vs.similarity_search_by_vector(embedding=embeddings.embed_query(question), k=4)
    state["context"] = docs
    return state