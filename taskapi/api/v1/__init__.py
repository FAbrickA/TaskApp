from fastapi import APIRouter

from .endpoints import router as router_
from ..utils import bind_routes

router = APIRouter(prefix="/v1")
bind_routes(router, [router_])

__all__ = [
    "router",
]