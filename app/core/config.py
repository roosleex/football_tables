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
    # Pro League, the Turkish Süper Lig, the Greek Super League, the Polish
    # Ekstraklasa, the Norwegian Eliteserien, the Danish Superliga, the
    # Cypriot First Division, the Swiss Super League, the Austrian Bundesliga,
    # the Nemzeti Bajnokság I, the Croatian Football League (HNL), the Swedish
    # Allsvenskan, the Scottish Premiership, the Romanian SuperLiga, the
    # Azerbaijan Premier League, the Israeli Premier League, the Slovenian
    # PrvaLiga, the Slovak Super Liga, the Bulgarian First League, the Serbian
    # SuperLiga, the Icelandic Besta deild, the League of Ireland Premier
    # Division, the Armenian Premier League, the Latvian Virslīga, the
    # Bosnian Premier League, the Kosovar Superleague, the Veikkausliiga,
    # the Kazakhstan Premier League, the Moldovan Super League, the Faroe
    # Islands Premier League and the Albanian Superliga).
    # OPENFOOT_API_KEY authenticates requests; FOOTAPI_MAX_REQUESTS_PER_MINUTE
    # controls its per-minute request budget.
    openfoot_api_key: str | None = None
    openfoot_base_url: str = "https://openfootapi.com"
    footapi_max_requests_per_minute: int = 60

    # thesportsdb.com integration: used for the Czech First League. The free
    # tier accepts the public key "123"; THESPORTSDB_MAX_REQUESTS_PER_MINUTE
    # controls its per-minute request budget (the free tier allows 30).
    thesportsdb_api_key: str = "123"
    thesportsdb_base_url: str = "https://www.thesportsdb.com/api/v1/json"
    thesportsdb_max_requests_per_minute: int = 30

    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


@lru_cache
def get_settings() -> Settings:
    """Return a cached, process-wide settings instance."""
    return Settings()