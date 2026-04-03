import json
from typing import Any
from urllib import request
from urllib.error import URLError, HTTPError


class LLMClient:
    def __init__(self, api_key: str | None, model: str, base_url: str, timeout_seconds: int = 15) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    def generate_reply(self, user_message: str) -> str | None:
        """Return model-generated text, or None when unavailable/failing."""
        if not self.enabled:
            return None

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Jarvis, a concise helpful assistant. "
                        "Do not execute tools directly; reply conversationally."
                    ),
                },
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.4,
        }

        req = request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                choices = body.get("choices", [])
                if not choices:
                    return None
                message = choices[0].get("message", {})
                content = message.get("content")
                if not isinstance(content, str):
                    return None
                return content.strip() or None
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError):
            return None
