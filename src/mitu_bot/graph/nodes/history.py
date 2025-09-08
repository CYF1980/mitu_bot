from ..state import AgentState

def store_history_node(state: AgentState) -> AgentState:
    """
    Store the latest user question and bot answer into the conversation history.
    """
    user_text = (state.get("text") or "").strip()
    answer_text = (state.get("answer_text") or "").strip()

    msgs_to_add = []
    if user_text:
        msgs_to_add.append({"role": "user", "content": user_text})
    if answer_text:
        msgs_to_add.append({"role": "assistant", "content": answer_text})

    if msgs_to_add:
        # Append new messages to existing ones
        state["messages"] = msgs_to_add

    return state
