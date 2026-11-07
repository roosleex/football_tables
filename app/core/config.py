"""Application configuration, loaded from environment variables or a ``.env`` file."""

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


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

    # SQLite storage: a snapshot of all standings, written by the refresh task.
    database_path: str = str(PROJECT_ROOT / "football_tables.db")

    # How often the background task re-fetches and persists standings.
    refresh_interval_seconds: int = 60

    # Form changes slowly, so refresh it less often than standings.
    form_refresh_interval_seconds: int = 600

    # Maximum football-data.org requests per minute (free tier: 10).
    max_requests_per_minute: int = 10

    # Competition codes to hide from the menu — second divisions, e.g. "ELC"
    # (Championship), "BL2" (2. Bundesliga), "SB" (Serie B), "FL2" (Ligue 2).
    excluded_league_codes: list[str] = ["ELC"]

    # openfootapi.com integration: a secondary standings source for leagues not
    # covered by football-data.org (the Ukrainian Premier League, the Belgian
    # Pro League and the Turkish Süper Lig). OPENFOOT_API_KEY authenticates
    # requests; FOOTAPI_MAX_REQUESTS_PER_MINUTE controls its per-minute budget.
    openfoot_api_key: str | None = None
    openfoot_base_url: str = "https://openfootapi.com"
    footapi_max_requests_per_minute: int = 60

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    """Return a cached, process-wide settings instance."""
    return Settings()