import uvicorn
from fastapi import FastAPI

from .api.v1 import router as router_v1
from .config import get_settings

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


if __name__ == '__main__':
    uvicorn.run(
        "taskapi.__main__:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["taskapi"],
        log_level="debug",
    )
    print(__file__)
