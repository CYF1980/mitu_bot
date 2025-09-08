from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState
from .nodes.asr import asr_node
from .nodes.retrieve import retrieve_node
from .nodes.generate import generate_node
from .nodes.tts import tts_node
from .nodes.guards import ensure_question
from .nodes.listen import listen_node
from .nodes.history import store_history_node

def build_graph(with_voice: bool = False):
    g = StateGraph(AgentState)
    # Nodes
    g.add_node("ensure_question", ensure_question)
    g.add_node("retrieve", retrieve_node)
    g.add_node("generate", generate_node)
    g.add_node("store_history", store_history_node)

    if with_voice:
        g.add_node("listen", listen_node)
        g.add_node("asr", asr_node)
        g.add_node("tts", tts_node)

    # Edges
    if with_voice:
        g.add_edge(START, "listen")
        g.add_edge("listen", "asr")
        g.add_edge("asr", "ensure_question")
    else:
        g.add_edge(START, "ensure_question")

    g.add_conditional_edges(
        "ensure_question",
        lambda s: "has_text" if s.get("text") else "no_text",
        {"has_text": "retrieve", "no_text": END},
    )

    g.add_edge("retrieve", "generate")
    g.add_edge("generate", "store_history")

    if with_voice:
        g.add_edge("store_history", "tts")
        g.add_edge("tts", END)
    else:
        g.add_edge("store_history", END)

    memory = MemorySaver()
    return g.compile(checkpointer=memory)