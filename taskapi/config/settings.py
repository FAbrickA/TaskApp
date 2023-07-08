import os

from pydantic import BaseSettings

from .utils import generate_random_token


class DefaultSettings(BaseSettings):
    # [App settings]
    APP_HOST: str = os.environ.get("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.environ.get("APP_PORT", 8000))

    # [Database settings]
    DATABASE_DB: str = os.environ.get("DATABASE_DB", "taskapi")
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "db")
    DATABASE_USER: str = os.environ.get("DATABASE_USER", "user123")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD", "password123")
    DATABASE_PORT: int = int(os.environ.get("DATABASE_PORT", 5432))

    # [Auth settings]
    SECRET_KEY: str = os.environ.get("SECRET_KEY", generate_random_token())
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    @property
    def database_settings(self) -> dict:
        """
        Get all database settings as dict
        """
        return {
            "database": self.DATABASE_DB,
            "host": self.DATABASE_HOST,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
            "port": self.DATABASE_PORT,
        }

    @property
    def database_uri_async(self):
        """
        Get async database connection uri
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"\
            .format(**self.database_settings)

    @property
    def database_uri_sync(self):
        """
        Get sync database connection uri
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}"\
            .format(**self.database_settings)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
