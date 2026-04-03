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