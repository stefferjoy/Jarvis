# Jarvis (Unified MVP)

Canonical project structure:
- `backend/` FastAPI orchestration and adapters
- `frontend/` Flutter mobile UI scaffold
- `AGENTS.md` project instructions

## Backend run

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
uvicorn app.main:app --reload --port 8000
```

### Backend environment variables

- `JARVIS_LLM_API_KEY` (required only for LLM conversational replies)
- `JARVIS_LLM_MODEL` (optional, default: `gpt-4.1-mini`)
- `JARVIS_LLM_BASE_URL` (optional, default: `https://api.openai.com/v1`)
- `JARVIS_SHORTCUTS_BRIDGE_URL` (optional, enables Apple Shortcuts handoff bridge)
- `JARVIS_SHORTCUTS_BRIDGE_TOKEN` (optional bearer token for bridge auth)
- `JARVIS_SHORTCUTS_BRIDGE_TIMEOUT_SECONDS` (optional, default: `8`)
- `JARVIS_HOME_BRIDGE_URL` (optional, enables home-device control bridge)
- `JARVIS_HOME_BRIDGE_TOKEN` (optional bearer token for home bridge auth)
- `JARVIS_HOME_BRIDGE_TIMEOUT_SECONDS` (optional, default: `8`)

If `JARVIS_LLM_API_KEY` is not set, deterministic Jarvis features still work and conversational replies use a graceful fallback message.

### Apple Shortcuts handoff bridge

The backend cannot directly execute Apple Shortcuts in most non-Apple runtimes. Instead, Jarvis now supports a bridge URL handoff:

1. Configure `JARVIS_SHORTCUTS_BRIDGE_URL` to an endpoint that can trigger Apple Shortcuts on your Apple device.
2. Optionally configure `JARVIS_SHORTCUTS_BRIDGE_TOKEN` for bearer auth.
3. From the frontend chat, send phrases like:
   - `run shortcut morning routine`
   - `start bedtime automation`

Frontend trigger path: chat message -> `POST /chat` -> deterministic orchestrator shortcut route -> shortcuts adapter bridge handoff.

### Home device control bridge

Direct Apple Home execution is not available from this backend runtime. Jarvis now supports a production-style bridge handoff:

1. Configure `JARVIS_HOME_BRIDGE_URL` to your home-control bridge endpoint.
2. Optionally configure `JARVIS_HOME_BRIDGE_TOKEN`.
3. Send chat commands such as:
   - `turn on bedroom light`
   - `switch on my room light`
   - `turn off bed lamp`

Frontend/external trigger path: chat message -> `POST /chat` -> deterministic device resolution + ambiguity handling -> home adapter bridge handoff.

## GitHub Codespaces

This repo now includes a minimal devcontainer at `.devcontainer/devcontainer.json`.

What you get immediately in Codespaces:
- Python 3.11 environment
- Backend dependencies installed via `pip install -e .` (from `backend/`)
- VS Code Python + Flutter extensions pre-installed

What still needs setup:
- Flutter SDK/toolchain installation before running the frontend app

### Codespaces startup commands

Backend (Terminal 1):

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend (Terminal 2, after Flutter SDK is installed in Codespaces):

```bash
cd frontend
flutter pub get
flutter run
```

## Frontend run

```bash
cd frontend
flutter pub get
flutter run
```

## Quick backend checks

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"turn on bedroom light"}'
```
