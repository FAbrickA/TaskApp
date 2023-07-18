import os
from asyncio import get_event_loop_policy
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app import get_app
from db.models import User
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
async def init_db() -> str:
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield TEST_DATABASE_URL

    os.remove(TEST_DATABASE_PATH)


@pytest.fixture
async def session(init_db) -> AsyncSession:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def client(session) -> AsyncClient:
    app = get_app()
    app.dependency_overrides[get_session] = lambda: session
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
async def user_sample(session) -> tuple[User, str]:
    # Generate user data
    username = str(uuid4())
    email = f"{username}@email.com"
    raw_password = str(uuid4())

    user = User(
        email=email,
    )
    user.set_password(raw_password)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user, raw_password
