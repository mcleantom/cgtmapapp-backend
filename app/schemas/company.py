from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict
from enum import Enum
from typing import Literal


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
    name: Optional[str]
    position: Optional[Point]
    category: Optional[ECompanyCategory]
    description: Optional[str]
    website: Optional[HttpUrl]
    logo: Optional[HttpUrl]


class CompanyInDB(Company):
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
