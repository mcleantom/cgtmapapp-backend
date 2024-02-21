from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings

from app.core.db_secret import get_secret

__all__ = ["Settings", "settings", "CGTMapBackendConfig"]


class CGTMapBackendConfig(BaseModel):
    pass


class Settings(BaseSettings):
    SQL_ALCHEMY_DATABASE_URI: PostgresDsn = Field(..., env="SQL_ALCHEMY_DATABASE_URI", default_factory=get_secret)


settings = Settings()
