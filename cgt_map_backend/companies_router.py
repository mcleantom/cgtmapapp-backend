from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from .db_models import Company, ECompanyCategory
from .pydantic_annotations import PydanticObjectId


class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CreateCompanyRequest(BaseModel):
    name: str
    position: Point
    category: ECompanyCategory
    description: str
    website: HttpUrl
    logo: HttpUrl


class CompanyResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    position: Point
    category: ECompanyCategory
    description: str
    website: HttpUrl
    logo: HttpUrl

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


def create_companies_router() -> APIRouter:
    router = APIRouter()

    @router.get("")
    async def get_companies() -> list[CompanyResponse]:
        companies = Company.objects().all()
        return [CompanyResponse.model_validate(company) for company in companies]

    @router.post("")
    async def create_company(company_request: CreateCompanyRequest) -> CompanyResponse:
        company = Company(
            name=company_request.name,
            position=company_request.position.coordinates,
            category=company_request.category,
            description=company_request.description,
            website=str(company_request.website),
            logo=str(company_request.logo),
        )
        company.save()

        return CompanyResponse(
            id=company._id,
            name=company.name,
            position=Point(**{"type": "Point", "coordinates": company.position}),
            category=company.category,
            description=company.description,
            website=company.website,
            logo=company.logo,
        )

    @router.delete("/{company_id}")
    async def delete_company(company_id: str) -> None:
        company = Company.objects.get(_id=company_id)
        company.delete()

    return router
