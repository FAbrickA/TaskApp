import os
from asyncio import get_event_loop_policy

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app import get_app
from db.models.base_model import BaseModel
from db.session import get_session

TEST_DATABASE_PATH = "test.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DATABASE_PATH}"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates event loop for tests.
    """
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session

    os.remove(TEST_DATABASE_PATH)


@pytest.fixture
async def client(db) -> AsyncClient:
    async def override_get_session() -> AsyncSession:
        try:
            yield db
        finally:
            await db.rollback()

    app = get_app()
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
