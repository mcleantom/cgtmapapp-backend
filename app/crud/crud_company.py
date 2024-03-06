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
            icon=obj_in.icon.unicode_string(),
            banner_image=obj_in.banner_image.unicode_string(),
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
            if "position" in update_data:
                update_data[
                    "position"
                ] = f"POINT({update_data['position']['coordinates'][0]} {update_data['position']['coordinates'][1]})"

        if "website" in update_data:
            update_data["website"] = update_data["website"].unicode_string()
        if "logo" in update_data:
            update_data["logo"] = update_data["logo"].unicode_string()
        if "icon" in update_data:
            update_data["icon"] = update_data["icon"].unicode_string()
        if "banner_image" in update_data:
            update_data["banner_image"] = update_data["banner_image"].unicode_string()

        return super().update(db, db_obj=db_obj, obj_in=update_data)


company = CRUDCompany(Company)
