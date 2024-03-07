from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.endpoints.companies import create_companies_router
from app.api.api_v1.endpoints.images import create_images_router
from app.core.config import CGTMapBackendConfig

__all__ = ["create_api"]


def create_api(config: CGTMapBackendConfig) -> FastAPI:
    app = FastAPI(
        title="CGT Map Backend",
        description="Backend for the CGT Map application",
        version="0.1.0",
    )
    app.include_router(create_companies_router(), prefix="/company", tags=["company"])
    app.include_router(create_images_router(config.image_router), prefix="/images", tags=["images"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
