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

## Endpoints
- `GET /health`
- `POST /chat` with JSON `{ "message": "..." }`
