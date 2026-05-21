"""Application settings loaded from environment variables."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration with defaults; override via .env or environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_API_KEY: str = ""
    LLM_TIMEOUT_SEC: int = 60
    LLM_MAX_RETRIES: int = 1

    # Data
    DATA_PATH: Path = Field(default=Path("data/processed/restaurants.parquet"))

    # Recommendation
    MAX_CANDIDATES: int = 10
    TOP_K_DEFAULT: int = 5

    # Budget bands (INR, cost for two)
    BUDGET_LOW_MAX: int = 400
    BUDGET_MEDIUM_MAX: int = 800

    # Prompt / validation limits
    MAX_REVIEW_CHARS: int = 200
    MAX_ADDITIONAL_PREF_CHARS: int = 500

    # Observability
    LOG_LEVEL: str = "INFO"


settings = Settings()
