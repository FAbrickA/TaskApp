from fastapi import APIRouter

from .endpoints import router as router_
from ..utils import bind_routes

API_PREFIX = "/api/v1"

router = APIRouter(prefix=API_PREFIX)
bind_routes(router, [router_])

__all__ = [
    "router",
    "API_PREFIX",
]