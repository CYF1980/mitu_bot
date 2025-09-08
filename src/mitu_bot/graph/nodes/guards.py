from ..state import AgentState

def ensure_question(state: AgentState) -> AgentState:
    if not state.get("text"):
        state["answer_text"] = "Sorry, I didn't catch that. Please ask a question."
    return state