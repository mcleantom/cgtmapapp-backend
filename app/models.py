from typing import Union

from geoalchemy2 import Geometry, WKBElement
from pydantic import ConfigDict
from sqlmodel import Column, Enum, Field, SQLModel

from app.schemas.company import ECompanyCategory

__all__ = ["Company", "init", "destruct"]


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
