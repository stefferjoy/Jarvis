from fastapi import APIRouter

from app.core.orchestrator import JarvisOrchestrator
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter()
orchestrator = JarvisOrchestrator()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    reply = orchestrator.handle_message(payload.message)
    return ChatResponse(reply=reply)
