import json
from urllib import request
from urllib.error import HTTPError, URLError

from app.config import HOME_BRIDGE_TIMEOUT_SECONDS, HOME_BRIDGE_TOKEN, HOME_BRIDGE_URL


def control_home_device(
    device_name: str,
    action: str,
    value: str | None = None,
    bridge_url: str | None = None,
    bridge_token: str | None = None,
    timeout_seconds: int | None = None,
) -> str:
    """Send deterministic home-control handoff to a configured bridge endpoint."""
    target_url = bridge_url or HOME_BRIDGE_URL
    token = bridge_token if bridge_token is not None else HOME_BRIDGE_TOKEN
    timeout = timeout_seconds or HOME_BRIDGE_TIMEOUT_SECONDS

    if not target_url:
        return (
            f"Home bridge unavailable for '{device_name}': set JARVIS_HOME_BRIDGE_URL "
            "to enable home-device control handoff."
        )

    payload = {
        "device_name": device_name,
        "action": action,
        "value": value,
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
                return f"Home bridge handoff sent: {action} '{device_name}'."
            return f"Home bridge handoff failed with HTTP status {status}."
    except (HTTPError, URLError, TimeoutError) as exc:
        return f"Home bridge handoff failed: {exc}."
