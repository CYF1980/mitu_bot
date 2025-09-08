from pathlib import Path
import os
from typing import Optional, List, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    llm_model: str = "gpt-4o-mini"
    embed_model: str = "text-embedding-3-large"
    chroma_dir: str = "tmp_context/chromadb"
    language: Literal["zh", "en", "auto"] = "auto"
    collection: str = "mitu-collection"
    default_prompt_version: str = "EricChoiceUsedCarsPrompt.yml"
    asr_prompt: Optional[str] = ("You are a used car sales assistant.")

    # ASR / TTS
    asr_model: str = "gpt-4o-mini-transcribe"
    tts_model: str = "gpt-4o-mini-tts"
    tts_voice: str = "nova"
    tts_out_path: str = "/tmp/mitu_tts.wav"

    # Audio capture
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    audio_sample_width_bytes: int = 2  # 16-bit

    # VAD parameters
    vad_frame_ms: int = 30
    vad_calibrate_sec: float = 0.5
    vad_silence_timeout_sec: float = 1.8
    vad_max_utterance_sec: float = 60.0
    vad_threshold_boost: float = 1.6

    # Playback candidates, in order
    audio_players: List[str] = ["afplay", "ffplay -autoexit -nodisp", "aplay"]

    greeting_text: str = "Hello, may I help you?"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
