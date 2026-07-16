from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse

from app.models import ChatRequest, ChatResponse
from app.llm import get_llm
from app.config import settings

router = APIRouter()


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest, _=Depends(verify_api_key)):
    llm = get_llm()
    result = llm.invoke(req.message)
    return ChatResponse(reply=result.content, session_id=req.session_id)


@router.post("/chat/stream")
async def chat_stream(req: ChatRequest, _=Depends(verify_api_key)):
    llm = get_llm()

    async def token_generator():
        async for chunk in llm.astream(req.message):
            yield chunk.content

    return StreamingResponse(token_generator(), media_type="text/plain")
