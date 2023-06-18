import os

from pydantic import BaseSettings


class DefaultSettings(BaseSettings):
    APP_HOST = os.environ.get("APP_HOST", "127.0.0.1")
    APP_PORT = os.environ.get("APP_PORT", 8000)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
