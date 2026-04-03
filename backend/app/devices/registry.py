import json
from pathlib import Path
from typing import Any

from app.devices.sample_devices import SAMPLE_DEVICES


class DeviceRegistry:
    def __init__(self, registry_path: Path) -> None:
        self.registry_path = registry_path
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            with self.registry_path.open("w", encoding="utf-8") as f:
                json.dump(SAMPLE_DEVICES, f, indent=2)

    def _load(self) -> list[dict[str, Any]]:
        try:
            with self.registry_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return SAMPLE_DEVICES

    def all_devices(self) -> list[dict[str, Any]]:
        return self._load()

    def find_matches(self, utterance: str, device_type: str | None = None) -> list[dict[str, Any]]:
        text = utterance.lower()
        matches: list[dict[str, Any]] = []
        for device in self._load():
            if device_type and device.get("type") != device_type:
                continue
            terms = [device.get("canonical_name", ""), *device.get("aliases", [])]
            if any(term and term.lower() in text for term in terms):
                matches.append(device)
        return matches

    def list_by_type(self, device_type: str) -> list[dict[str, Any]]:
        return [device for device in self._load() if device.get("type") == device_type]
