from ..state import AgentState
from ...adapters.llm_openai import get_llm
from pathlib import Path
import yaml
from ...config.settings import settings

def _load_prompt():
    base_dir = Path(__file__).resolve().parents[2] / "prompts"
    file = base_dir / settings.default_prompt_version
    with open(file, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("system", ""), data.get("user", "")

def generate_node(state: AgentState) -> AgentState:
    llm = get_llm()
    system_tmpl, user_tmpl = _load_prompt()
    context = "\n\n".join(doc.page_content for doc in state.get("context", []) or [])
    question = state.get("text", "")

    system_content = system_tmpl.replace("{{context}}", context)
    user_content = user_tmpl.replace("{{question}}", question)
    history = state.get("messages", []) or []

    messages = [
        {"role": "system", "content": system_content}] + history + [
        {"role": "user", "content": user_content}
    ]
    resp = llm.invoke(messages)
    answer = getattr(resp, "content", str(resp)).strip()
    state["answer_text"] = answer

    return state
