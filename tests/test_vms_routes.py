from fastapi.testclient import TestClient


def create_vm(client: TestClient) -> str:
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
    return response.json()["id"]


def test_create_vm_returns_real_created_vm(client: TestClient) -> None:
    vm_id = create_vm(client)

    response = client.get(f"/api/v1/vms/{vm_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vm_id
    assert data["name"] == "demo-vm"
    assert data["status"] == "ACTIVE"


def test_list_vms_returns_created_vm(client: TestClient) -> None:
    vm_id = create_vm(client)

    response = client.get("/api/v1/vms")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["items"][0]["id"] == vm_id
    assert data["items"][0]["name"] == "demo-vm"


def test_stop_then_start_vm_updates_status(client: TestClient) -> None:
    vm_id = create_vm(client)

    stop_response = client.post(f"/api/v1/vms/{vm_id}/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["status"] == "SHUTOFF"

    start_response = client.post(f"/api/v1/vms/{vm_id}/start")
    assert start_response.status_code == 200
    assert start_response.json()["status"] == "ACTIVE"


def test_reboot_vm_keeps_vm_active(client: TestClient) -> None:
    vm_id = create_vm(client)

    response = client.post(f"/api/v1/vms/{vm_id}/reboot")

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "reboot"
    assert data["status"] == "ACTIVE"


def test_update_vm_metadata_merges_values(client: TestClient) -> None:
    vm_id = create_vm(client)

    patch_payload = {"metadata": {"env": "dev"}}
    patch_response = client.patch(
        f"/api/v1/vms/{vm_id}/metadata",
        json=patch_payload,
    )

    assert patch_response.status_code == 200
    data = patch_response.json()
    assert data["metadata"]["owner"] == "parth"
    assert data["metadata"]["env"] == "dev"


def test_delete_vm_removes_record(client: TestClient) -> None:
    vm_id = create_vm(client)

    delete_response = client.delete(f"/api/v1/vms/{vm_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "DELETED"

    get_response = client.get(f"/api/v1/vms/{vm_id}")
    assert get_response.status_code == 404
    assert get_response.json()["error"]["code"] == "vm_not_found"


def test_get_vm_returns_structured_404_for_missing_vm(client: TestClient) -> None:
    response = client.get("/api/v1/vms/missing-vm")

    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "vm_not_found"
    assert data["error"]["message"] == "VM 'missing-vm' was not found"


def test_start_vm_returns_409_when_already_active(client: TestClient) -> None:
    vm_id = create_vm(client)

    response = client.post(f"/api/v1/vms/{vm_id}/start")

    assert response.status_code == 409
    data = response.json()
    assert data["error"]["code"] == "invalid_vm_state"
    assert data["error"]["details"]["action"] == "start"


def test_reboot_vm_returns_409_when_vm_is_shutoff(client: TestClient) -> None:
    vm_id = create_vm(client)

    stop_response = client.post(f"/api/v1/vms/{vm_id}/stop")
    assert stop_response.status_code == 200

    reboot_response = client.post(f"/api/v1/vms/{vm_id}/reboot")

    assert reboot_response.status_code == 409
    data = reboot_response.json()
    assert data["error"]["code"] == "invalid_vm_state"
    assert data["error"]["details"]["current_status"] == "SHUTOFF"


def test_create_vm_validation_failure_returns_structured_error(
    client: TestClient,
) -> None:
    payload = {
        "name": "ab",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    response = client.post("/api/v1/vms", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "request_validation_error"
    assert data["error"]["message"] == "Request validation failed"