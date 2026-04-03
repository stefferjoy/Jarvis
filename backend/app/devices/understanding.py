from dataclasses import dataclass
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

    def resolve(self, utterance: str, device_type: str | None = None) -> DeviceMatchResult:
        normalized = utterance.lower()
        candidates = self.registry.all_devices()

        if device_type:
            candidates = [d for d in candidates if d.get("type") == device_type]

        # Primary score: canonical/alias direct mentions.
        scored: list[tuple[int, dict[str, Any]]] = []
        for device in candidates:
            score = self._score_device(device, normalized)
            if score > 0:
                scored.append((score, device))

        if not scored:
            # Fallback by room + device type token (e.g. "bedroom light").
            room_type_matches = [
                d
                for d in candidates
                if self._room_token_in_utterance(d, normalized)
                and (d.get("type", "") in normalized or device_type is not None)
            ]
            if room_type_matches:
                if len(room_type_matches) == 1:
                    return DeviceMatchResult(status="single", matches=room_type_matches)
                return DeviceMatchResult(status="ambiguous", matches=room_type_matches)

            # Generic type phrase fallback (e.g. "turn on light") for clarification flow.
            if device_type and device_type in normalized:
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

        canonical_name = str(device.get("canonical_name", "")).lower()
        aliases = [str(alias).lower() for alias in device.get("aliases", [])]
        room = str(device.get("room", "")).lower()
        device_type = str(device.get("type", "")).lower()

        if canonical_name and canonical_name in normalized_utterance:
            score += 8

        for alias in aliases:
            if alias and alias in normalized_utterance:
                score += 6

        if room and room in normalized_utterance:
            score += 3

        if device_type and device_type in normalized_utterance:
            score += 2

        return score

    @staticmethod
    def _room_token_in_utterance(device: dict[str, Any], normalized_utterance: str) -> bool:
        room = str(device.get("room", "")).lower()
        return bool(room and room in normalized_utterance)
