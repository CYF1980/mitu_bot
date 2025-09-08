# src/mitu_bot/init_env.py
import os
from .config.settings import settings

if settings.openai_api_key:
    os.environ.setdefault("OPENAI_API_KEY", settings.openai_api_key)
