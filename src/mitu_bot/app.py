from __future__ import annotations
import typer
from pathlib import Path
from typing import Optional
from .config.settings import settings
from .dataio.ingest import ingest_csv_to_chroma
from .graph.build import build_graph
from .graph.nodes.tts import tts_node
from . import init_env # setup env vars

app = typer.Typer(help="mitu-bot CLI")

@app.command()
def ingest(path: str = typer.Option(..., help="Path to CSV/Doc"),
           rebuild: bool = typer.Option(False, help="Rebuild vectorstore")):
    p = Path(path)
    if not p.exists():
        raise typer.BadParameter(f"Not found: {p}")
    count = ingest_csv_to_chroma(str(p), rebuild=rebuild)
    typer.echo(f"Ingested {count} documents into collection '{settings.collection}'.")

@app.command()
def chat(text: Optional[str] = typer.Option(None, help="If provided, run single-turn Q&A; otherwise start interactive loop"),
         voice: bool = typer.Option(False, "--voice", "-v", help="Enable voice I/O (mic + TTS)")):
    """
    Chat with the bot.
    - Provide --text for single-turn.
    - Omit --text to start an interactive loop (Ctrl+C to exit).
    - Add --voice to use microphone + TTS (interactive only).
    """
    graph = build_graph(with_voice=voice)

    # Single-turn (backward compatible)
    if text is not None:
        out = graph.invoke(
                {"input_mode": "text", "text": text},
                config={"configurable": {"thread_id": "single"}}
        )
        print(out.get("answer_text", ""))
        return

    # Interactive REPL
    if not voice:
        typer.echo("💬 Interactive chat started. Press Ctrl+C to exit.\n")
        try:
            while True:
                try:
                    q = input("You > ").strip()
                except EOFError:
                    typer.echo("\nBye!")
                    break
                if not q:
                    continue
                out = graph.invoke(
                    {"input_mode": "text", "text": q},
                    config={"configurable": {"thread_id": "repl"}}
                )
                a = out.get("answer_text", "")
                print(f"Bot > {a}\n")
        except KeyboardInterrupt:
            typer.echo("\nBye!")
        return

    # Voice chat
    typer.echo("🎙️ Voice chat started. Speak after calibration; Ctrl+C to exit.\n")

    try:
        while True:
            out = graph.invoke(
                {"input_mode": "audio"},
                config={"configurable": {"thread_id": "voice"}}
            )
            answer = out.get("answer_text", "")
            print(f"Bot > {answer}\n")
            # If silence, ensure_question may have set a gentle message; we only print when non-empty.
    except KeyboardInterrupt:
        typer.echo("\nBye!")

@app.command()
def diag():
    """Simple health check."""
    from .adapters.vectorstore_chroma import get_vectorstore
    vs = get_vectorstore()
    typer.echo(f"Vectorstore loaded. Collection: {settings.collection}")

def main():
    app()

if __name__ == "__main__":
    main()
