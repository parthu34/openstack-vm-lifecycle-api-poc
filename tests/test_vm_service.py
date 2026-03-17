import pytest

from app.core.exceptions import InvalidVMStateError, VMNotFoundError
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.providers.mock_openstack import MockOpenStackProvider
from app.services.vm_service import VMService


def create_demo_vm(service: VMService) -> str:
    vm = service.create_vm(
        VMCreateRequest(
            name="demo-vm",
            image="ubuntu-22.04",
            flavor="m1.small",
            network="private-net",
            metadata={"owner": "parth"},
        )
    )
    return vm.id


def test_get_vm_raises_domain_not_found_error() -> None:
    service = VMService(MockOpenStackProvider())

    with pytest.raises(VMNotFoundError):
        service.get_vm("missing-vm")


def test_start_vm_raises_invalid_state_when_already_active() -> None:
    service = VMService(MockOpenStackProvider())
    vm_id = create_demo_vm(service)

    with pytest.raises(InvalidVMStateError):
        service.start_vm(vm_id)


def test_stop_vm_raises_invalid_state_when_already_stopped() -> None:
    service = VMService(MockOpenStackProvider())
    vm_id = create_demo_vm(service)

    service.stop_vm(vm_id)

    with pytest.raises(InvalidVMStateError):
        service.stop_vm(vm_id)


def test_reboot_vm_raises_invalid_state_when_shutoff() -> None:
    service = VMService(MockOpenStackProvider())
    vm_id = create_demo_vm(service)

    service.stop_vm(vm_id)

    with pytest.raises(InvalidVMStateError):
        service.reboot_vm(vm_id)


def test_update_metadata_raises_not_found_for_missing_vm() -> None:
    service = VMService(MockOpenStackProvider())

    with pytest.raises(VMNotFoundError):
        service.update_metadata(
            "missing-vm",
            VMMetadataUpdateRequest(metadata={"env": "dev"}),
        )