from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings



engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass