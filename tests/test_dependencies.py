from app.core.config import settings
from app.core.exceptions import ProviderConfigurationError
from app.dependencies import get_provider
from app.providers.mock_openstack import MockOpenStackProvider
from app.providers.real_openstack import RealOpenStackProvider


def test_get_provider_returns_mock_provider_when_mode_is_mock() -> None:
    original_mode = settings.provider_mode
    get_provider.cache_clear()

    try:
        settings.provider_mode = "mock"
        provider = get_provider()
        assert isinstance(provider, MockOpenStackProvider)
    finally:
        settings.provider_mode = original_mode
        get_provider.cache_clear()


def test_get_provider_returns_real_provider_when_mode_is_openstack() -> None:
    original_mode = settings.provider_mode
    get_provider.cache_clear()

    try:
        settings.provider_mode = "openstack"
        provider = get_provider()
        assert isinstance(provider, RealOpenStackProvider)
    finally:
        settings.provider_mode = original_mode
        get_provider.cache_clear()


def test_get_provider_raises_for_unsupported_mode() -> None:
    original_mode = settings.provider_mode
    get_provider.cache_clear()

    try:
        settings.provider_mode = "invalid-mode"

        try:
            get_provider()
            assert False, "Expected ProviderConfigurationError to be raised"
        except ProviderConfigurationError as exc:
            assert exc.code == "provider_configuration_error"
    finally:
        settings.provider_mode = original_mode
        get_provider.cache_clear()