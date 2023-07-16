from .auth.endpoints import router as router_auth
from .health.endpoints import router as router_health

__all__ = [
    "router_auth",
    "router_health",
]