from typing import Generator, Annotated
from fastapi import Depends
from app.db.engine import engine
from sqlmodel import Session


__all__ = [
    "SessionDep",
]


def get_db() -> Generator:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
