# src/mitu_bot/graph/state.py
from typing import TypedDict, List, Literal, Optional
from langchain_core.documents import Document
from typing_extensions import Annotated
from langgraph.graph.message import add_messages, AnyMessage

class AgentState(TypedDict, total=False):
    input_mode: Literal["text", "audio"]
    audio_bytes: Optional[bytes]     # PCM bytes from mic
    text: str                        # User input text (from text or ASR)
    lang: Literal["zh", "en"]
    context: List[Document]
    answer_text: str
    audio_out: Optional[bytes]       # WAV bytes from TTS
    audio_out_path: Optional[str]    # Path to TTS WAV file

    # Chat history for LLM (messages with role/content)
    messages: Annotated[list[AnyMessage], add_messages]
