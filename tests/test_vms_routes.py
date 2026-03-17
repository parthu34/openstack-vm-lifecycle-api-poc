from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_vm_returns_placeholder_response() -> None:
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
        "key_name": "demo-key",
        "metadata": {"owner": "parth"},
        "user_data": "#!/bin/bash\necho hello",
    }

    response = client.post("/api/v1/vms", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "mock-vm-001"
    assert data["name"] == "demo-vm"
    assert data["status"] == "BUILD"


def test_list_vms_returns_empty_collection() -> None:
    response = client.get("/api/v1/vms")

    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["count"] == 0


def test_get_vm_returns_404_placeholder() -> None:
    response = client.get("/api/v1/vms/vm-123")

    assert response.status_code == 404
    assert response.json()["detail"] == "VM 'vm-123' was not found"


def test_start_vm_returns_action_response() -> None:
    response = client.post("/api/v1/vms/vm-123/start")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "vm-123"
    assert data["action"] == "start"
    assert data["status"] == "ACTIVE"


def test_stop_vm_returns_action_response() -> None:
    response = client.post("/api/v1/vms/vm-123/stop")

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "stop"
    assert data["status"] == "SHUTOFF"


def test_reboot_vm_returns_action_response() -> None:
    response = client.post("/api/v1/vms/vm-123/reboot")

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "reboot"
    assert data["status"] == "REBOOT"


def test_update_vm_metadata_returns_updated_metadata() -> None:
    payload = {
        "metadata": {
            "env": "dev",
            "owner": "parth",
        }
    }

    response = client.patch("/api/v1/vms/vm-123/metadata", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "vm-123"
    assert data["metadata"]["env"] == "dev"
    assert data["metadata"]["owner"] == "parth"


def test_delete_vm_returns_action_response() -> None:
    response = client.delete("/api/v1/vms/vm-123")

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "delete"
    assert data["status"] == "DELETED"


def test_create_vm_validation_failure_when_name_too_short() -> None:
    payload = {
        "name": "ab",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    response = client.post("/api/v1/vms", json=payload)

    assert response.status_code == 422