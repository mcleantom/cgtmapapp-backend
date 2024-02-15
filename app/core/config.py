from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, BaseModel

__all__ = ["Settings", "settings", "CGTMapBackendConfig"]


class CGTMapBackendConfig(BaseModel):
    pass


class Settings(BaseSettings):
    SQL_ALCHEMY_DATABASE_URI: PostgresDsn


settings = Settings()
