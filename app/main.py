"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import router as api_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Standings for the major European football leagues.",
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