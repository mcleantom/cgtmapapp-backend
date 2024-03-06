import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from geoalchemy2.shape import to_shape
from shapely import to_geojson
from sqlmodel import select

from app.api.deps import SessionDep
from app.crud.crud_company import company as crud_company
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyInDB, CompanyUpdate

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
        icon=db_company.icon,
        banner_image=db_company.banner_image,
    )


def create_companies_router() -> APIRouter:
    router = APIRouter()

    @router.post("", response_model=CompanyInDB)
    def create_company(session: SessionDep, company: CompanyCreate):
        db_company = crud_company.create(session, obj_in=company)
        return convert_db_company_to_pydantic(db_company)

    @router.get("", response_model=list[CompanyInDB])
    def read_companies(session: SessionDep, skip: int = 0, limit: int = 10):
        statement = select(Company).offset(skip).limit(limit)
        companies = session.exec(statement).all()
        p_companies = [convert_db_company_to_pydantic(c) for c in companies]
        return p_companies

    @router.put("/{company_id}", response_model=CompanyInDB)
    def update_company(session: SessionDep, company_id: int, company: CompanyUpdate):
        db_company = crud_company.get(session, id=company_id)
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not found")
        db_company = crud_company.update(session, db_obj=db_company, obj_in=company)
        return convert_db_company_to_pydantic(db_company)

    @router.delete("/{company_id}", response_class=JSONResponse)
    def delete_company(session: SessionDep, company_id: int):
        db_company = crud_company.remove(session, id=company_id)
        if not db_company:
            raise HTTPException(status_code=404, detail="Company not found")
        return JSONResponse(content={"detail": "Company deleted"})

    return router
