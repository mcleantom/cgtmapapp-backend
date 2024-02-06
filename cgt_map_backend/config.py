from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["CGTMapBackendConfig", "MongoDBConfig"]


class MongoDBConfig(BaseSettings):
    uri: str
    db_name: str

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="MONGO__",
    )


class CGTMapBackendConfig(BaseModel):
    title: str = "CGT Map Backend API"
    mongo: MongoDBConfig = MongoDBConfig()
