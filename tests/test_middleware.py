from fastapi.testclient import TestClient


def test_health_response_contains_request_headers(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time-Ms" in response.headers
    assert response.headers["X-Request-ID"] != ""


def test_request_id_is_preserved_when_sent_by_client(
    client: TestClient,
) -> None:
    response = client.get("/health", headers={"X-Request-ID": "custom-req-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "custom-req-123"


def test_error_response_also_contains_request_headers(client: TestClient) -> None:
    response = client.get("/api/v1/vms/missing-vm")

    assert response.status_code == 404
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time-Ms" in response.headers