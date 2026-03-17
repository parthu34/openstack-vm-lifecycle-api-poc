from functools import lru_cache

from fastapi import Depends

from app.core.config import settings
from app.core.exceptions import ProviderConfigurationError
from app.providers.base import VMProvider
from app.providers.mock_openstack import MockOpenStackProvider
from app.providers.real_openstack import RealOpenStackProvider
from app.services.vm_service import VMService


@lru_cache
def get_provider() -> VMProvider:
    if settings.provider_mode == "mock":
        return MockOpenStackProvider()

    if settings.provider_mode == "openstack":
        return RealOpenStackProvider(settings)

    raise ProviderConfigurationError(settings.provider_mode)


def get_vm_service(provider: VMProvider = Depends(get_provider)) -> VMService:
    return VMService(provider)