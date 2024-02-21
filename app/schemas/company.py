from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, HttpUrl

__all__ = [
    "Point",
    "ECompanyCategory",
    "Company",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyInDB",
]


class Point(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]

    def to_wkt(self) -> str:
        return f"POINT({self.coordinates[0]} {self.coordinates[1]})"


class ECompanyCategory(str, Enum):
    Consulting = "Consulting"
    Accelerator = "Accelerator"
    Startup = "Startup"


class Company(BaseModel):
    name: str
    position: Point
    category: ECompanyCategory
    description: str
    website: HttpUrl
    logo: HttpUrl


class CompanyCreate(BaseModel):
    name: str
    position: Point
    category: ECompanyCategory
    description: str
    website: HttpUrl
    logo: HttpUrl


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[Point] = None
    category: Optional[ECompanyCategory] = None
    description: Optional[str] = None
    website: Optional[HttpUrl] = None
    logo: Optional[HttpUrl] = None


class CompanyInDB(Company):
    id: int

    model_config = ConfigDict(from_attributes=True)
