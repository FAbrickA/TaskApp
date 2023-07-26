import os
import datetime as dt
from asyncio import get_event_loop_policy
from uuid import uuid4

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.v1.endpoints.auth.utils import get_authorization_headers, create_access_token
from app import get_app
from db.models import User, Task
from db.models.base_model import BaseModel
from db.session import get_session
from tests.utils import generate_user, generate_task

TEST_DATABASE_PATH = "test.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TEST_DATABASE_PATH}"

engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False)


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
def raw_password():
    """
    Generate raw_password for User
    """
    return str(uuid4())


@pytest.fixture
async def user(session, raw_password) -> User:
    """
    Generate User and save it to testing database
    """
    yield await generate_user(session, raw_password)


@pytest.fixture
async def user_factory(session):
    """
    Create factory to generate more users if one is not enough
    """
    async def _generate_user() -> User:
        return await generate_user(session)

    yield _generate_user


@pytest.fixture
async def auth_client(session, client, user) -> AsyncClient:
    """
    Get authorized client
    """
    # Create access token
    payload = {"email": user.email}
    expires_delta = dt.timedelta(minutes=30)
    access_token = create_access_token(payload, expires_delta)

    # Set authorization headers
    authorization_headers = get_authorization_headers(access_token)
    client.headers.update(authorization_headers)

    yield client


@pytest.fixture
async def task(session, user) -> Task:
    """
    Create Task, bind it to current user and save to database.
    """
    task = generate_task()
    task.user_id = user.id
    session.add(task)
    await session.commit()
    await session.refresh(task)

    yield task


@pytest.fixture
def task_factory():
    """
    Create Task factory.
    Task is not saved to database.
    """

    return generate_task
