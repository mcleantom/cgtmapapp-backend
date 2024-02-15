from fastapi import APIRouter
from app.models import (
    Company,
)
from app.schemas.company import CompanyCreate, CompanyInDB
from app.api.deps import SessionDep
from app.crud.crud_company import company as crud_company
from sqlmodel import select
from geoalchemy2.shape import to_shape
from shapely import to_geojson
import json


__all__ = ["create_companies_router"]


def convert_db_company_to_pydantic(db_company: Company) -> CompanyInDB:
    return CompanyInDB(
        id=db_company.id,
        name=db_company.name,
        position=json.loads(to_geojson(to_shape(db_company.position))),
        category=db_company.category,
        description=db_company.description,
        website=db_company.website,
        logo=db_company.logo,
    )


def create_companies_router() -> APIRouter:
    router = APIRouter()

    @router.get("", response_model=list[CompanyInDB])
    def read_companies(session: SessionDep, skip: int = 0, limit: int = 10):
        statement = select(Company).offset(skip).limit(limit)
        companies = session.exec(statement).all()
        p_companies = [convert_db_company_to_pydantic(c) for c in companies]
        return p_companies

    @router.post("", response_model=CompanyInDB)
    def create_company(session: SessionDep, company: CompanyCreate):
        db_company = crud_company.create(session, obj_in=company)
        return convert_db_company_to_pydantic(db_company)

    return router
