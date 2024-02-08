from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .companies_router import create_companies_router
from .config import CGTMapBackendConfig

db_str = "mongodb+srv://tom_mclean:password@cgt-app.37mlsd9.mongodb.net/test?retryWrites=true"


def create_app(config: CGTMapBackendConfig) -> FastAPI:
    config.mongo.connect()

    app = FastAPI(
        title=config.title,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    companies_router = create_companies_router()
    app.include_router(companies_router, prefix="/company", tags=["company"])

    return app
