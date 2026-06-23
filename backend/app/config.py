from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # Database
    database_url: str

    # JWT Auth
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS — comma-separated list of allowed origins, e.g. "http://localhost:5173"
    # Use "*" only for development
    cors_origins: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance (avoids re-reading .env on every call)."""
    return Settings()


settings = get_settings()
