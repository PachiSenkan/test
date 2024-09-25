import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

from app.config import settings


engine = create_engine(settings.db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
