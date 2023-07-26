from .auth.endpoints import router as router_auth
from .health.endpoints import router as router_health
from .tasks.endpoints import router as router_tasks

__all__ = [
    "router_auth",
    "router_health",
    "router_tasks",
]