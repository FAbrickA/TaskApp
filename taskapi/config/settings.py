import os

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    APP_HOST = os.environ.get("APP_HOST", "127.0.0.1")
    APP_PORT = os.environ.get("APP_PORT", 8000)

    DATABASE_DB = os.environ.get("DATABASE_DB", "taskapi")
    DATABASE_HOST = os.environ.get("DATABASE_HOST", "db")
    DATABASE_USER = os.environ.get("DATABASE_USER", "user123")
    DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password123")
    DATABASE_PORT = os.environ.get("DATABASE_PORT", 5432)

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
