from functools import lru_cache

from app.core.config import settings
from app.providers.base import VMProvider
from app.providers.mock_openstack import MockOpenStackProvider


@lru_cache
def get_provider() -> VMProvider:
    if settings.provider_mode == "mock":
        return MockOpenStackProvider()

    raise ValueError(
        f"Unsupported provider_mode '{settings.provider_mode}'. "
        "Only 'mock' is available at this stage."
    )