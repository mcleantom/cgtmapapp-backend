from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings

from app.core.db_secret import get_secret

__all__ = ["Settings", "settings", "CGTMapBackendConfig", "ImageRouterConfig"]


class ImageRouterConfig(BaseModel):
    bucket_name: str
    cloudfront_url: str


class CGTMapBackendConfig(BaseModel):
    image_router: ImageRouterConfig


class Settings(BaseSettings):
    SQL_ALCHEMY_DATABASE_URI: PostgresDsn = Field(..., env="SQL_ALCHEMY_DATABASE_URI", default_factory=get_secret)


settings = Settings()
