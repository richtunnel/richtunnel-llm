from fastapi import APIRouter, Depends

from app.models import ChatRequest, ChatResponse
from app.routes.chat import verify_api_key
from app.agent import run_agent

router = APIRouter()


@router.post("/agent/chat", response_model=ChatResponse)
async def agent_chat(req: ChatRequest, _=Depends(verify_api_key)):
    reply = run_agent(req.message, req.session_id)
    return ChatResponse(reply=reply, session_id=req.session_id)
