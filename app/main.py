from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference
from scalar_fastapi.scalar_fastapi import Layout, Theme

from app.routes import chat, agent

app = FastAPI(title="Local LLM Service", docs_url=None, redoc_url=None)

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(agent.router, prefix="/api", tags=["agent"])

# Scalar ships its own compiled Tailwind/Vue bundle, so layout tweaks need
# !important to beat its scoped selectors, and hover states need explicit
# durations since its own reset just declares `transition: all` at 0s.
_DOCS_CUSTOM_CSS = """
html {
  scroll-behavior: smooth;
}

/* Scalar's default section padding (90px/48px) is what makes the page feel
   sparse — tighten it without touching the grid/column layout itself. */
.section {
  padding: 32px 24px !important;
  gap: 16px !important;
}
.section-header-wrapper {
  gap: 20px !important;
}
.section-header {
  margin-bottom: 8px !important;
}

/* Sidebar tag groups (chat/agent/Models) mount their child list with no
   transition at all, so opening one snaps the whole nav instantly. Fading
   it in on mount smooths that without needing to fake a height animation. */
li.group\/item > ul {
  transition: opacity 0.15s ease-out;
}
@starting-style {
  li.group\/item > ul {
    opacity: 0;
  }
}

/* Give sidebar/nav hover + active states an actual duration instead of the
   instant 0s default, so highlighting a link doesn't feel like a hard cut. */
.sidebar button,
.sidebar a,
nav button,
nav a {
  transition: background-color 0.15s ease, color 0.15s ease, opacity 0.15s ease !important;
}

/* Drop the "Powered by Scalar" sidebar footer link (and its now-empty
   wrapper, so it doesn't leave a blank gap below the MCP buttons). */
div:has(> a[href="https://www.scalar.com"]) {
  display: none !important;
}

/* Scalar's collapsed-tag "Show More" button pulls itself up 48px (relative
   positioning) to sit inside its section's default 48px bottom padding.
   We shrank that padding above, so the button now floats up over whatever
   card sits above it instead of below it. Drop the offset so it sits in
   normal flow. */
.show-more {
  top: 0 !important;
  margin-top: 8px;
}
"""


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
        show_developer_tools="never",
        custom_css=_DOCS_CUSTOM_CSS,
    )


@app.get("/health")
def health():
    return {"status": "ok"}


# Chat UI — built via `npm run build` in frontend/. Mounted last so it only
# catches requests that don't match /api, /docs, or /health above.
_FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
app.mount("/", StaticFiles(directory=_FRONTEND_DIST, html=True), name="frontend")
