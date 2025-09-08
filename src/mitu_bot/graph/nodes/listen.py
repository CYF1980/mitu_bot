from ..state import AgentState
from ...utils.audio import record_until_silence

def listen_node(state: AgentState) -> AgentState:
    """
    Capture audio from mic until silence, then write raw PCM bytes into state.
    If not in audio mode, do nothing.
    """
    if state.get("input_mode") != "audio":
        return state

    audio_bytes = record_until_silence()
    # Put bytes into state (empty bytes if nothing captured)
    state["audio_bytes"] = audio_bytes or b""
    return state
