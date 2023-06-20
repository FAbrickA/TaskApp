from fastapi import FastAPI

from api.v1 import router as router_v1
from config import get_settings

settings = get_settings()


def bind_routers(application: FastAPI):
    application.include_router(router_v1)


def get_app() -> FastAPI:
    application = FastAPI(
        title="Task Api",
        version="0.1.0",
    )
    bind_routers(application)
    return application


app = get_app()
