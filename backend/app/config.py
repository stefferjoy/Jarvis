import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
MEMORY_FILE = DATA_DIR / "memory.json"
DEVICES_FILE = DATA_DIR / "devices.json"

LLM_API_KEY = os.getenv("JARVIS_LLM_API_KEY")
LLM_MODEL = os.getenv("JARVIS_LLM_MODEL", "gpt-4.1-mini")
LLM_BASE_URL = os.getenv("JARVIS_LLM_BASE_URL", "https://api.openai.com/v1")

SHORTCUTS_BRIDGE_URL = os.getenv("JARVIS_SHORTCUTS_BRIDGE_URL")
SHORTCUTS_BRIDGE_TOKEN = os.getenv("JARVIS_SHORTCUTS_BRIDGE_TOKEN")
SHORTCUTS_BRIDGE_TIMEOUT_SECONDS = int(os.getenv("JARVIS_SHORTCUTS_BRIDGE_TIMEOUT_SECONDS", "8"))
