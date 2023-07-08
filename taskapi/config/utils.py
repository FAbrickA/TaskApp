import os
import secrets

from .settings import DefaultSettings


def get_settings() -> DefaultSettings:
    env = os.environ.get("ENV", "local")
    if env == "local":
        return DefaultSettings()
    # ...
    # space for other settings
    # ...
    return DefaultSettings()  # fallback to default


def generate_random_token():
    """ Generate crypto strong random token """
    number_of_bytes = 16
    return secrets.token_hex(number_of_bytes)  # length = number_of_bytes * 2
