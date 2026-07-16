from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi.scalar_fastapi import Layout, Theme

from app.routes import chat, agent

app = FastAPI(title="Local LLM Service", docs_url=None, redoc_url=None)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(agent.router, prefix="/api", tags=["agent"])


@app.get("/docs", include_in_schema=False)
def docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        theme=Theme.PURPLE,
        layout=Layout.MODERN,
        dark_mode=True,
        force_dark_mode_state="dark",
        hide_client_button=True,
        telemetry=False,
    )


@app.get("/health")
def health():
    return {"status": "ok"}
