from langchain_ollama import ChatOllama
from app.config import settings


def get_llm(temperature: float = 0.2):
    """Return a ChatOllama client pointed at the local Ollama server."""
    return ChatOllama(
        model=settings.model_name,
        base_url=settings.ollama_base_url,
        temperature=temperature,
    )
