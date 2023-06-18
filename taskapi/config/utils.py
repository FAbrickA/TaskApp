import os

from .settings import DefaultSettings


def get_settings() -> DefaultSettings:
    env = os.environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    # ...
    # space for other settings
    # ...
    return DefaultSettings()  # fallback to default
