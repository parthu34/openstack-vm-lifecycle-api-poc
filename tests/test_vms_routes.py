from fastapi.testclient import TestClient


def test_create_vm_returns_real_created_vm(client: TestClient) -> None:
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
    assert data["name"] == "demo-vm"
    assert data["status"] == "ACTIVE"
    assert data["image"] == "ubuntu-22.04"
    assert len(data["id"]) > 0


def test_list_vms_returns_created_vm(client: TestClient) -> None:
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    create_response = client.post("/api/v1/vms", json=payload)
    created_vm = create_response.json()

    response = client.get("/api/v1/vms")

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["items"][0]["id"] == created_vm["id"]
    assert data["items"][0]["name"] == "demo-vm"


def test_get_vm_returns_created_vm(client: TestClient) -> None:
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    create_response = client.post("/api/v1/vms", json=payload)
    vm_id = create_response.json()["id"]

    response = client.get(f"/api/v1/vms/{vm_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == vm_id
    assert data["name"] == "demo-vm"


def test_stop_then_start_vm_updates_status(client: TestClient) -> None:
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    create_response = client.post("/api/v1/vms", json=payload)
    vm_id = create_response.json()["id"]

    stop_response = client.post(f"/api/v1/vms/{vm_id}/stop")
    assert stop_response.status_code == 200
    assert stop_response.json()["status"] == "SHUTOFF"

    start_response = client.post(f"/api/v1/vms/{vm_id}/start")
    assert start_response.status_code == 200
    assert start_response.json()["status"] == "ACTIVE"

    get_response = client.get(f"/api/v1/vms/{vm_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "ACTIVE"


def test_reboot_vm_keeps_vm_active(client: TestClient) -> None:
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    create_response = client.post("/api/v1/vms", json=payload)
    vm_id = create_response.json()["id"]

    response = client.post(f"/api/v1/vms/{vm_id}/reboot")

    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "reboot"
    assert data["status"] == "ACTIVE"


def test_update_vm_metadata_merges_values(client: TestClient) -> None:
    create_payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
        "metadata": {"owner": "parth"},
    }

    create_response = client.post("/api/v1/vms", json=create_payload)
    vm_id = create_response.json()["id"]

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
    payload = {
        "name": "demo-vm",
        "image": "ubuntu-22.04",
        "flavor": "m1.small",
        "network": "private-net",
    }

    create_response = client.post("/api/v1/vms", json=payload)
    vm_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/vms/{vm_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "DELETED"

    get_response = client.get(f"/api/v1/vms/{vm_id}")
    assert get_response.status_code == 404


def test_get_vm_returns_404_for_missing_vm(client: TestClient) -> None:
    response = client.get("/api/v1/vms/missing-vm")

    assert response.status_code == 404
    assert response.json()["detail"] == "VM 'missing-vm' was not found"


def test_create_vm_validation_failure_when_name_too_short(
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