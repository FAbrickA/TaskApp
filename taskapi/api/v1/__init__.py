from fastapi import APIRouter

from .endpoints import router as router_
from .config import API_PREFIX
from ..utils import bind_routes

router = APIRouter(prefix=API_PREFIX)
bind_routes(router, [router_])

__all__ = [
    "router",
    "API_PREFIX",
]