from typing import Union

from pydantic import HttpUrl, ConfigDict
from sqlmodel import Field, SQLModel, Column, Enum
from geoalchemy2 import Geometry, WKBElement
from app.schemas.company import ECompanyCategory
from geoalchemy2.types import Geometry as GeometryType

__all__ = ["Company", "CompanyCreate", "init", "destruct"]


class CompanyCreate(SQLModel, table=False):
    name: str
    position: GeometryType
    category: ECompanyCategory
    description: str
    website: HttpUrl
    logo: HttpUrl

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Company(SQLModel, table=True):
    id: Union[int, None] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    position: WKBElement = Field(sa_column=Column(Geometry("POINT")))
    category: ECompanyCategory = Field(sa_column=Column(Enum(ECompanyCategory)))
    description: str = Field(max_length=500)
    website: str = Field(max_length=100)
    logo: str = Field(max_length=100)

    model_config = ConfigDict(arbitrary_types_allowed=True)


def init():
    from app.db.engine import engine

    SQLModel.metadata.create_all(bind=engine)


def destruct():
    from app.db.engine import engine

    SQLModel.metadata.drop_all(bind=engine)
