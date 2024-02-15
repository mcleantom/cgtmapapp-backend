from sqlmodel import create_engine

from app.core.config import settings

engine = create_engine(settings.SQL_ALCHEMY_DATABASE_URI.unicode_string())
