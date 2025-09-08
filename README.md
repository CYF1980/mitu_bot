# mitu-bot

🚀 A simple demo **LangGraph RAG chatbot** with Chroma vector store and pluggable ASR/TTS.  
Supports **text chat**, **voice chat**, and **custom domain knowledge ingestion**.

---

## ✨ Features

- **Retrieval-Augmented Generation (RAG)** with [ChromaDB](https://docs.trychroma.com/).
- **LangGraph-powered orchestration** with modular state graphs.
- **Pluggable ASR/TTS** using OpenAI APIs (`gpt-4o-mini-transcribe`, `gpt-4o-mini-tts`).
- **Voice interaction** 🎙️ (mic input + real-time speech synthesis).
- **Custom dataset ingestion**: load your CSVs/documents into vector search.
- **Configurable prompts** (swap YAML prompt templates per use case).
- **CLI interface** with [Typer](https://typer.tiangolo.com/).

---

## 📦 Installation
#### (If running on Raspberry Pi)
```bash
sudo apt update
sudo apt install -y portaudio19-dev libasound2-dev python3-dev
```
### Clone and Install
```bash
git clone https://github.com/CYF1980/mitu_bot.git
cd mitu_bot
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

Copy the environment template and add your OpenAI key:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY=your_key_here
```

---

## 🚀 Quickstart

### 1. Ingest data into Chroma
```bash
python -m src.mitu_bot.app ingest --path src/mitu_bot/data/docs/EricChoiceUsedCars.csv --rebuild
```

### 2. Ask a single question
```bash
python -m src.mitu_bot.app chat --text "Which is your most cheap car?"
```

### 3. Interactive REPL
```bash
python -m src.mitu_bot.app chat
```

### 4. Voice chat 🎤
```bash
python -m src.mitu_bot.app chat --voice
```

---

## 🗂 Project Structure

```
mitu_bot/
├── pyproject.toml          # Dependencies and build metadata
├── README.md               # Project docs
├── src/mitu_bot/           # Main source
│   ├── adapters/           # LLM, embeddings, vectorstore adapters
│   ├── config/             # Pydantic settings
│   ├── data/               # Sample datasets (CSV)
│   ├── dataio/             # Ingestion + loaders
│   ├── graph/              # LangGraph state + nodes
│   ├── prompts/            # Prompt YAML templates
│   ├── utils/              # Audio utilities
│   └── app.py              # CLI entrypoint
└── tmp_context/            # Chroma persistence
```

---

## ⚙️ Configuration

All runtime settings are in [`src/mitu_bot/config/settings.py`](src/mitu_bot/config/settings.py).  
Key options:

- `llm_model`: default `"gpt-4o-mini"`
- `embed_model`: `"text-embedding-3-large"`
- `chroma_dir`: vectorstore persistence dir
- `tts_model`, `tts_voice`: voice synthesis options
- `default_prompt_version`: which YAML prompt to use

---

## 🛠 Development

Run tests:

```bash
pytest
```

Lint & format:

```bash
ruff check .
mypy src
```

---

## 🔮 Extending

- Add new **prompt templates** under `src/mitu_bot/prompts/`.
- Plug in other **vectorstores** (e.g. FAISS, Weaviate) by editing `adapters/vectorstore_*`.
- Extend **graph nodes** (`graph/nodes/`) to add guards, memory, or custom tools.
- Swap **ASR/TTS backends** (e.g. Whisper, Coqui TTS).

---

## 📜 License

MIT License. See [LICENSE](LICENSE).
