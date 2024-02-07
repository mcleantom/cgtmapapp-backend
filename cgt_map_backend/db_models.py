from datetime import datetime
from enum import Enum

from bson.objectid import ObjectId
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, EnumField, ObjectIdField, PointField, StringField


class MongoBaseDocument(Document):
    meta = {"abstract": True}
    _id: ObjectId = ObjectIdField(required=True, primary_key=True, default=ObjectId)
    _date_created: datetime = DateTimeField(default=datetime.utcnow)


class ECompanyCategory(str, Enum):
    Consulting = "Consulting"
    Accelerator = "Accelerator"
    Startup = "Startup"


class Company(MongoBaseDocument):
    name: str = StringField(required=True, index=True)
    position = PointField(required=True, index=True)
    category: ECompanyCategory = EnumField(ECompanyCategory, required=True, index=True)
    description: str = StringField(required=True)
    website: str = StringField(required=True)
    logo: str = StringField(required=True)
