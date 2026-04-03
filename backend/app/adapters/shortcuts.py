import json
from typing import Any
from urllib import request
from urllib.error import HTTPError, URLError

from app.config import (
    SHORTCUTS_BRIDGE_TIMEOUT_SECONDS,
    SHORTCUTS_BRIDGE_TOKEN,
    SHORTCUTS_BRIDGE_URL,
)


def run_shortcut(
    name: str,
    params: dict[str, Any] | None = None,
    bridge_url: str | None = None,
    bridge_token: str | None = None,
    timeout_seconds: int | None = None,
) -> str:
    """Send a shortcut handoff request to a configured bridge endpoint.

    This is a production-ready bridge path for environments where direct Apple
    Shortcuts execution is not possible from the backend runtime.
    """
    target_url = bridge_url or SHORTCUTS_BRIDGE_URL
    token = bridge_token if bridge_token is not None else SHORTCUTS_BRIDGE_TOKEN
    timeout = timeout_seconds or SHORTCUTS_BRIDGE_TIMEOUT_SECONDS

    if not target_url:
        return (
            "Shortcut handoff unavailable: set JARVIS_SHORTCUTS_BRIDGE_URL "
            "to enable Apple Shortcuts bridge execution."
        )

    payload: dict[str, Any] = {
        "shortcut": name,
        "params": params or {},
    }

    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = request.Request(
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            if 200 <= status < 300:
                return f"Shortcut handoff sent: '{name}'."
            return f"Shortcut handoff failed with HTTP status {status}."
    except (HTTPError, URLError, TimeoutError) as exc:
        return f"Shortcut handoff failed: {exc}."
