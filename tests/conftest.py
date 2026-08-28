import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from service.db import Base, get_db
from service.main import app
from service.settings import Settings

test_settings = Settings(
    _env_file=".env.test",
    postgres_host="localhost",
    postgres_port=5433,
)


@pytest_asyncio.fixture(scope="session")
async def engine():
    engine = create_async_engine(test_settings.database_url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(engine):
    async_session = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.rollback()
        for _, table in Base.metadata.tables.items():
            query = delete(table)
            await session.execute(query)
        await session.commit()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
