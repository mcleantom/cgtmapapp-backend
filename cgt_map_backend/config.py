from abc import ABC, abstractmethod
from typing import Annotated, Literal, Union

from mongoengine import connect
from mongomock import MongoClient
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from cgt_map_backend.db_uri_secret import get_secret

__all__ = ["CGTMapBackendConfig", "MongoDBUri", "MongoDBMock"]


class MongoDBConfigBase(BaseSettings, ABC):
    @abstractmethod
    def connect(self):
        pass


class MongoDBUri(MongoDBConfigBase):
    type: Literal["URI"] = Field("URI", env="MONGO_TYPE")
    uri: str = Field(..., env="MONGO_URI", default_factory=get_secret)
    db: str = Field("CGT-App", env="MONGO_DB")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="MONGO_",
        env_nested_delimiter="__",
    )

    def connect(self):
        connect(host=self.uri)


class MongoDBMock(MongoDBConfigBase):
    type: Literal["MOCK"] = Field("MOCK", env="MONGO_TYPE")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="MONGO_",
        env_nested_delimiter="__",
    )

    def connect(self):
        connect("mongoenginetest", host="mongodb://localhost", mongo_client_class=MongoClient)


MongoDBConfig = Annotated[Union[MongoDBUri, MongoDBMock], Field(discriminator="type")]


class CGTMapBackendConfig(BaseModel):
    title: str = "CGT Map Backend API"
    mongo: MongoDBConfig
