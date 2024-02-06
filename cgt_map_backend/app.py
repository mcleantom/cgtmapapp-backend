from .config import CGTMapBackendConfig
from fastapi import FastAPI
from .companies_router import create_companies_router
from mongoengine import connect
from .db_models import Company

db_str = "mongodb+srv://tom_mclean:password@cgt-app.37mlsd9.mongodb.net/test?retryWrites=true"


def create_app(config: CGTMapBackendConfig) -> FastAPI:
    connect(host=config.mongo.uri)

    app = FastAPI(
        title=config.title,
    )

    companies_router = create_companies_router()
    app.include_router(companies_router, prefix="/companies")

    return app
