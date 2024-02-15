from fastapi import FastAPI
from app.api.api_v1.endpoints.companies import create_companies_router
from app.core.config import CGTMapBackendConfig
from app.models import init, destruct

__all__ = ["create_api"]


def create_api(config: CGTMapBackendConfig) -> FastAPI:
    app = FastAPI(
        title="CGT Map Backend",
        description="Backend for the CGT Map application",
        version="0.1.0",
    )
    app.include_router(create_companies_router(), prefix="/company", tags=["company"])

    @app.on_event("startup")
    async def startup_event():
        init()

    @app.on_event("shutdown")
    async def shutdown_event():
        destruct()

    return app
