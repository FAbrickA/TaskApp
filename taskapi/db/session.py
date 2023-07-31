from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from config import get_settings


class SessionManager:
    """
    Singleton class to manage database sessions
    """

    _instance = None
    engine = None

    def __init__(self):
        self.refresh()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_session_maker(self) -> async_sessionmaker:
        return async_sessionmaker(self.engine, expire_on_commit=False)

    def refresh(self):
        self.engine = create_async_engine(get_settings().database_uri_async, echo=True, future=True)


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        yield session
