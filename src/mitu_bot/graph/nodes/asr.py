import io
import wave
from openai import OpenAI
from ...config.settings import settings
from ..state import AgentState

def _wav_from_pcm_bytes(pcm: bytes, sr: int, channels: int, sampwidth: int) -> bytes:
    """ Convert raw PCM bytes to WAV bytes in-memory. """
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        wf.writeframes(pcm)
    return buf.getvalue()

def asr_node(state: AgentState) -> AgentState:
    if state.get("input_mode") != "audio":
        return state

    audio_bytes = state.get("audio_bytes") or b""
    if not audio_bytes:
        state["text"] = ""
        return state

    wav_bytes = _wav_from_pcm_bytes(
        audio_bytes,
        sr=settings.audio_sample_rate,
        channels=settings.audio_channels,
        sampwidth=settings.audio_sample_width_bytes,
    )

    client = OpenAI(api_key=settings.openai_api_key)
    try:
        # use in-memory bytes
        fobj = io.BytesIO(wav_bytes)
        fobj.name = "input.wav"  # OpenAI API expects a file name
        transcript = client.audio.transcriptions.create(
            model=settings.asr_model,
            file=fobj,
            prompt=settings.asr_prompt
        )
        text = (transcript.text or "").strip()
        state["text"] = text
    except Exception as e:
        state["text"] = ""
        state["answer_text"] = f"[ASR] To text failed:{e}"
    print(f"[ASR] Detected speech: {state.get('text','')}")
    return state
