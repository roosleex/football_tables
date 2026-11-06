"""Application configuration, loaded from environment variables or a ``.env`` file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the Football Tables backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Football Tables"
    api_prefix: str = "/api"

    # football-data.org integration. Set FOOTBALL_DATA_API_KEY to switch from the
    # bundled demo data to live standings.
    football_data_api_key: str | None = None
    football_data_base_url: str = "https://api.football-data.org/v4"
    http_timeout_seconds: float = 10.0

    # Live standings are cached to stay within football-data.org rate limits.
    standings_cache_ttl_seconds: int = 300

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    """Return a cached, process-wide settings instance."""
    return Settings()