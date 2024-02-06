from mongoengine.document import Document
from mongoengine.fields import StringField, PointField, DateField, DateTimeField, ObjectIdField, EnumField
from datetime import datetime
from bson.objectid import ObjectId
from enum import Enum


class MongoBaseDocument(Document):
    meta = {'abstract': True}
    _id: ObjectId = ObjectIdField(required=True, primary_key=True, default=ObjectId)
    _date_created: datetime = DateTimeField(default=datetime.utcnow)


class ECompanyCategory(str, Enum):
    Consulting = "Consulting"


class Company(MongoBaseDocument):
    name: str = StringField(required=True, index=True)
    position = PointField(required=True, index=True)
    category: ECompanyCategory = EnumField(ECompanyCategory, required=True, index=True)
    description: str = StringField()
    website: str = StringField()
