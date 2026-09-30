from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "FitBuddy"

    database_url: str = "sqlite:///./fitbuddy.db"

    use_gemini: bool = False

    gemini_api_key: str | None = None

    workout_model: str = "gemini-3.8-flash"

    nutrition_model: str = "gemini-3.8-flash"

    admin_key: str = Field(
        default="change-me-for-local-admin"
    )

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()