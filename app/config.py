from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "qwen2.5:7b"
    api_key: str = "change-me"  # simple shared-secret auth; swap for real auth in production

    class Config:
        env_file = ".env"


settings = Settings()
