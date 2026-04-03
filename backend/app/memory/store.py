import json
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, memory_path: Path) -> None:
        self.memory_path = memory_path
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.memory_path.exists():
            self._write({"facts": [], "recent_messages": []})

    def _read(self) -> dict[str, Any]:
        try:
            with self.memory_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {"facts": [], "recent_messages": []}

    def _write(self, payload: dict[str, Any]) -> None:
        with self.memory_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def append_recent_message(self, message: str) -> None:
        data = self._read()
        recent = data.get("recent_messages", [])
        recent.append(message)
        data["recent_messages"] = recent[-20:]
        self._write(data)

    def remember_fact(self, fact: str) -> None:
        data = self._read()
        facts = data.get("facts", [])
        if fact not in facts:
            facts.append(fact)
        data["facts"] = facts
        self._write(data)

    def list_facts(self) -> list[str]:
        data = self._read()
        return data.get("facts", [])
