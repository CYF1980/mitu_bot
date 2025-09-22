# src/mitu_bot/graph/nodes/greeting_voice.py
from ..state import AgentState
from ...config.settings import settings
from .tts import tts_node

def greeting_node(state: AgentState) -> AgentState:
    """
    Play a greeting message using TTS when starting a voice chat.
    """
    try:
        local_state: AgentState = {"answer_text": settings.greeting_text}
        tts_node(local_state)  # Call TTS node to generate greeting audio
        # Merge audio output back into state
        for key in ("audio_out", "audio_out_path"):
            if key in local_state:
                state[key] = local_state[key]
        # mark greeted so subsequent invokes skip greeting
        state["has_greeted"] = True
    except Exception as e:
        state["answer_text"] = f"[TTS] Greeting failed: {e}"
    return state
