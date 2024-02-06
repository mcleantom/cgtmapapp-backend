from fastapi import APIRouter
from .db_models import Company, ECompanyCategory
import json
from pydantic import BaseModel, HttpUrl


class CreateCompanyRequest(BaseModel):
    name: str
    position: tuple[float, float]
    category: ECompanyCategory
    description: str
    website: HttpUrl


def create_companies_router() -> APIRouter:
    router = APIRouter()

    @router.get('/companies')
    async def get_companies():
        companies = Company.objects().all()
        return json.loads(companies.to_json())

    @router.post('/companies')
    async def create_company(company_request: CreateCompanyRequest):
        company = Company(
            name=company_request.name,
            position=company_request.position,
            category=company_request.category,
            description=company_request.description,
            website=str(company_request.website)
        )
        company.save()
        return json.loads(company.to_json())

    return router
