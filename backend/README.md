# Jarvis Backend MVP

## Run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8000
```

## LLM configuration (optional)

- `JARVIS_LLM_API_KEY` to enable model-backed conversational replies
- `JARVIS_LLM_MODEL` optional override (default `gpt-4.1-mini`)
- `JARVIS_LLM_BASE_URL` optional override (default `https://api.openai.com/v1`)

If no API key is set, deterministic Jarvis flows (memory/device/camera/shortcuts) continue to work and chat falls back gracefully.

## Apple Shortcuts bridge (first real integration path)

Set these environment variables:

- `JARVIS_SHORTCUTS_BRIDGE_URL` (required for bridge execution)
- `JARVIS_SHORTCUTS_BRIDGE_TOKEN` (optional bearer token)
- `JARVIS_SHORTCUTS_BRIDGE_TIMEOUT_SECONDS` (optional; default `8`)

Usage:
- Send `run shortcut <name>` or `start <name> automation` to `POST /chat`.
- Orchestrator resolves shortcut intent deterministically and forwards to the bridge adapter.

If bridge config is missing or bridge execution fails, Jarvis returns a graceful fallback message.

## Home device control bridge (first real home integration path)

Set these environment variables:

- `JARVIS_HOME_BRIDGE_URL` (required for bridge execution)
- `JARVIS_HOME_BRIDGE_TOKEN` (optional bearer token)
- `JARVIS_HOME_BRIDGE_TIMEOUT_SECONDS` (optional; default `8`)

Usage:
- Send `turn on bedroom light`, `switch on my room light`, or similar light commands to `POST /chat`.
- Orchestrator keeps device registry + ambiguity handling deterministic and forwards resolved actions to the home adapter bridge.

If bridge config is missing or bridge execution fails, Jarvis returns a graceful fallback message.

## Endpoints
- `GET /health`
- `POST /chat` with JSON `{ "message": "..." }`
