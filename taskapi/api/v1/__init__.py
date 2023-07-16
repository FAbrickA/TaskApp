from fastapi import APIRouter

from .endpoints import router_auth, router_health
from .config import API_PREFIX
from ..utils import bind_routes

router = APIRouter(prefix=API_PREFIX)
bind_routes(router, [
    router_auth,
    router_health,
])

__all__ = [
    "router",
    "API_PREFIX",
]