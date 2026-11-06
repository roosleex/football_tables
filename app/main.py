"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import router as api_router
from app.core.config import Settings, get_settings
from app.core.leagues import DEFAULT_LEAGUES, LeagueCatalog
from app.db.sqlite import StandingsRepository
from app.services.base import StandingsProvider
from app.services.demo_provider import DemoProvider
from app.services.football_data_provider import FootballDataProvider
from app.services.refresh_scheduler import RefreshScheduler
from app.services.standings_service import StandingsService


def build_provider(settings: Settings) -> StandingsProvider:
    if settings.football_data_api_key:
        return FootballDataProvider(settings)
    return DemoProvider()


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        repository = StandingsRepository(settings.database_path)
        repository.init_schema()

        provider = build_provider(settings)
        catalog = LeagueCatalog(DEFAULT_LEAGUES)
        scheduler = RefreshScheduler(
            provider,
            repository,
            catalog,
            interval_seconds=settings.refresh_interval_seconds,
            form_interval_seconds=settings.form_refresh_interval_seconds,
        )

        # Populate the league catalog before serving (fast: demo is instant, live
        # is a couple of list requests). Standings are fetched in the background.
        scheduler.refresh_leagues()

        # In demo mode (no network) also load standings synchronously so the API
        # is immediately ready and tests are deterministic.
        if provider.source == "demo":
            scheduler.refresh_standings()

        app.state.standings_service = StandingsService(repository, catalog)

        thread = scheduler.start()
        try:
            yield
        finally:
            scheduler.stop()
            thread.join(timeout=5)

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Standings for the major European football leagues.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/", include_in_schema=False)
    def root() -> dict[str, str]:
        return {
            "service": settings.app_name,
            "docs": "/docs",
            "health": f"{settings.api_prefix}/health",
        }

    return app


app = create_app()