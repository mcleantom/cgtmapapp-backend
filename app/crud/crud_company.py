from typing import Any, Dict, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

__all__ = ["company"]


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        position_wkt = f"POINT({obj_in.position.coordinates[0]} {obj_in.position.coordinates[1]})"
        db_obj = Company(
            name=obj_in.name,
            position=position_wkt,
            category=obj_in.category,
            description=obj_in.description,
            website=obj_in.website.unicode_string(),
            logo=obj_in.logo.unicode_string(),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Company,
        obj_in: Union[CompanyUpdate, Dict[str, Any]],
    ) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
            update_data[
                "position"
            ] = f"POINT({update_data['position']['coordinates'][0]} {update_data['position']['coordinates'][1]})"
        return super().update(db, db_obj=db_obj, obj_in=update_data)


company = CRUDCompany(Company)
