import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_provider
from app.main import app
from app.providers.mock_openstack import MockOpenStackProvider


@pytest.fixture
def mock_provider() -> MockOpenStackProvider:
    provider = MockOpenStackProvider()
    app.dependency_overrides[get_provider] = lambda: provider
    yield provider
    app.dependency_overrides.clear()


@pytest.fixture
def client(mock_provider: MockOpenStackProvider) -> TestClient:
    with TestClient(app) as test_client:
        yield test_client