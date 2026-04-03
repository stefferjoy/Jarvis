from dataclasses import dataclass
import re
from typing import Any

from app.devices.registry import DeviceRegistry


@dataclass
class DeviceMatchResult:
    status: str
    matches: list[dict[str, Any]]


class DeviceUnderstanding:
    """Unified device understanding layer for canonical names, aliases, rooms, and types."""

    def __init__(self, registry: DeviceRegistry) -> None:
        self.registry = registry
        self.type_aliases = {
            "light": ["light", "lights", "lamp", "lamps"],
            "camera": ["camera", "cam", "cams", "feed", "doorbell"],
        }

    def resolve(self, utterance: str, device_type: str | None = None) -> DeviceMatchResult:
        normalized = self._normalize(utterance)
        candidates = self.registry.all_devices()

        if device_type:
            candidates = [d for d in candidates if d.get("type") == device_type]

        # Primary score: canonical/alias + room/type token matching.
        scored: list[tuple[int, dict[str, Any]]] = []
        for device in candidates:
            score = self._score_device(device, normalized)
            if score > 0:
                scored.append((score, device))

        if not scored:
            # Fallback by room + type token (e.g. "bedroom lamp", "front door feed").
            room_type_matches = [
                d
                for d in candidates
                if self._room_token_in_utterance(d, normalized)
                and self._type_token_in_utterance(str(d.get("type", "")), normalized)
            ]
            if room_type_matches:
                if len(room_type_matches) == 1:
                    return DeviceMatchResult(status="single", matches=room_type_matches)
                return DeviceMatchResult(status="ambiguous", matches=room_type_matches)

            # Generic type phrase fallback (e.g. "turn on lights") for clarification flow.
            if device_type and self._type_token_in_utterance(device_type, normalized):
                type_matches = [d for d in candidates if d.get("type") == device_type]
                if len(type_matches) == 1:
                    return DeviceMatchResult(status="single", matches=type_matches)
                if len(type_matches) > 1:
                    return DeviceMatchResult(status="ambiguous", matches=type_matches)

            return DeviceMatchResult(status="none", matches=[])

        scored.sort(key=lambda item: item[0], reverse=True)
        best_score = scored[0][0]
        best_devices = [device for score, device in scored if score == best_score]

        if len(best_devices) == 1:
            return DeviceMatchResult(status="single", matches=best_devices)

        return DeviceMatchResult(status="ambiguous", matches=best_devices)

    def _score_device(self, device: dict[str, Any], normalized_utterance: str) -> int:
        score = 0

        canonical_name = self._normalize(str(device.get("canonical_name", "")))
        aliases = [self._normalize(str(alias)) for alias in device.get("aliases", [])]
        room = self._normalize(str(device.get("room", "")))
        device_type = self._normalize(str(device.get("type", "")))

        if canonical_name and canonical_name in normalized_utterance:
            score += 8
        score += self._specificity_bonus(canonical_name, normalized_utterance)

        for alias in aliases:
            if alias and alias in normalized_utterance:
                score += 6
            score += self._specificity_bonus(alias, normalized_utterance)

        if room and self._room_token_in_utterance(device, normalized_utterance):
            score += 3

        if device_type and self._exact_type_token_in_utterance(device_type, normalized_utterance):
            score += 2

        return score

    @staticmethod
    def _room_token_in_utterance(device: dict[str, Any], normalized_utterance: str) -> bool:
        room = str(device.get("room", "")).lower()
        room_variants = [room]
        if room == "bedroom":
            room_variants.extend(["my room", "bed room"])
        if room == "entry":
            room_variants.extend(["front door", "door", "foyer"])
        return any(variant and variant in normalized_utterance for variant in room_variants)

    def _type_token_in_utterance(self, device_type: str, normalized_utterance: str) -> bool:
        aliases = self.type_aliases.get(device_type, [device_type])
        return any(alias in normalized_utterance for alias in aliases if alias)

    @staticmethod
    def _exact_type_token_in_utterance(device_type: str, normalized_utterance: str) -> bool:
        exact_aliases = [device_type, f"{device_type}s"]
        return any(alias in normalized_utterance for alias in exact_aliases)

    @staticmethod
    def _specificity_bonus(phrase: str, utterance: str) -> int:
        distinctive_tokens = ["lamp", "camera", "cam", "feed", "doorbell"]
        for token in distinctive_tokens:
            if token in utterance and token in phrase:
                return 3
        return 0

    @staticmethod
    def _normalize(text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", text.lower())).strip()
