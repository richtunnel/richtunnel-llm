# Local LLM Stack — FastAPI + LangChain/LangGraph + Ollama

A runnable starter: a local LLM served by Ollama, wrapped in a FastAPI service,
with a LangGraph agent (tools + memory) on top.

## 1. Install Ollama and pull a model

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

ollama serve                 # start the server (may already be running as a service)
ollama pull qwen2.5:7b       # tool-capable model — required for the agent to work
```

Verify it's up:
```bash
curl http://localhost:11434/api/generate -d '{"model":"qwen2.5:7b","prompt":"hello","stream":false}'
```

## 2. Set up the Python environment

```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # edit if you want a different model or API key
```

## 3. Run the API

```bash
uvicorn app.main:app --reload --port 8000
```

## 4. Test it

In a second terminal:
```bash
python test_requests.py
```

Or manually:
```bash
# plain chat
curl -X POST http://localhost:8000/api/chat \
  -H "x-api-key: change-me" -H "Content-Type: application/json" \
  -d '{"message": "What is Prisma used for?"}'

# agent with tools + memory
curl -X POST http://localhost:8000/api/agent/chat \
  -H "x-api-key: change-me" -H "Content-Type: application/json" \
  -d '{"message": "What'\''s the weather in Dallas?", "session_id": "s1"}'

# streaming chat
curl -N -X POST http://localhost:8000/api/chat/stream \
  -H "x-api-key: change-me" -H "Content-Type: application/json" \
  -d '{"message": "Write two sentences about local LLMs."}'
```

## Project layout

```
app/
├── main.py          # FastAPI app + router registration
├── config.py        # settings (model name, Ollama URL, API key) from .env
├── models.py        # request/response schemas
├── llm.py           # ChatOllama client factory
├── tools.py         # agent tools (weather stub, docs-search stub)
├── agent.py         # LangGraph ReAct agent + per-session memory
└── routes/
    ├── chat.py      # /api/chat and /api/chat/stream
    └── agent.py     # /api/agent/chat
```

## Where to extend this

- **Real tools**: replace the stubs in `app/tools.py` with real API calls or a
  retriever (see the RAG example in the full guide for adding a Chroma vector
  store as a tool).
- **Persistent memory**: swap `MemorySaver` in `app/agent.py` for
  `SqliteSaver` or `PostgresSaver` so agent memory survives a restart.
- **Auth**: the `x-api-key` header check in `routes/chat.py` is a placeholder —
  replace with real auth (JWT, OAuth, etc.) before shipping anywhere real.
- **A different/fine-tuned model**: change `MODEL_NAME` in `.env` to any model
  pulled into Ollama, including a fine-tuned model you've converted to GGUF
  and registered with `ollama create`.
