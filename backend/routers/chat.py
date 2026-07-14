from fastapi import APIRouter, HTTPException

from schemas.chat import ChatRequest, ChatResponse
from services.chat_service import get_chat_reply

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    history = [h.model_dump() for h in payload.history]
    try:
        reply, references = get_chat_reply(payload.message, history)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return ChatResponse(reply=reply, references=references)
