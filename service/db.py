"""Database engine, session factory, and the ORM declarative base."""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from .settings import settings

engine = create_async_engine(url=settings.database_url)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db():
    """FastAPI dependency that yields a request-scoped DB session."""
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    """Base class for all ORM models."""
