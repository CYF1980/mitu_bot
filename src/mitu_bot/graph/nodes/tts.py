import os
from openai import OpenAI
from ...config.settings import settings
from ..state import AgentState
from ...utils.audio import play_wav_with_system

def tts_node(state: AgentState) -> AgentState:
    text = state.get("answer_text") or ""
    if not text:
        state["audio_out"] = None
        return state

    print(f"[TTS] Generating speech for answer: {text}")
    client = OpenAI(api_key=settings.openai_api_key)
    out_path = settings.tts_out_path
    try:
        # Streaming response to file
        with client.audio.speech.with_streaming_response.create(
            model=settings.tts_model,
            voice=settings.tts_voice,
            input=text,
            response_format="wav",
        ) as response:
            response.stream_to_file(out_path)

        state["audio_out_path"] = out_path
        # Play immediately
        play_wav_with_system(out_path)

        with open(out_path, "rb") as f:
            state["audio_out"] = f.read()
    except Exception as e:
        state["audio_out"] = None
        state["answer_text"] = state.get("answer_text", "") + f"\n[TTS] To speech failed:{e}"
    return state
