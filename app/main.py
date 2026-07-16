from fastapi import FastAPI

from app.routes import chat, agent

app = FastAPI(title="Local LLM Service")

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(agent.router, prefix="/api", tags=["agent"])


@app.get("/health")
def health():
    return {"status": "ok"}
