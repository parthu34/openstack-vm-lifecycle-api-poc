from uuid import uuid4

from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.providers.base import VMProvider


class MockOpenStackProvider(VMProvider):
    def __init__(self) -> None:
        self._vms: dict[str, VMResponse] = {}

    def create_vm(self, payload: VMCreateRequest) -> VMResponse:
        vm_id = uuid4().hex

        vm = VMResponse(
            id=vm_id,
            name=payload.name,
            status="ACTIVE",
            image=payload.image,
            flavor=payload.flavor,
            network=payload.network,
            key_name=payload.key_name,
            metadata=payload.metadata,
        )

        self._vms[vm_id] = vm
        return vm

    def list_vms(self) -> VMListResponse:
        items = list(self._vms.values())
        return VMListResponse(items=items, count=len(items))

    def get_vm(self, vm_id: str) -> VMResponse:
        vm = self._vms.get(vm_id)
        if vm is None:
            raise KeyError(vm_id)
        return vm

    def start_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)

        updated_vm = vm.model_copy(update={"status": "ACTIVE"})
        self._vms[vm_id] = updated_vm

        return VMActionResponse(
            id=vm_id,
            action="start",
            status=updated_vm.status,
            message="VM started successfully",
        )

    def stop_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)

        updated_vm = vm.model_copy(update={"status": "SHUTOFF"})
        self._vms[vm_id] = updated_vm

        return VMActionResponse(
            id=vm_id,
            action="stop",
            status=updated_vm.status,
            message="VM stopped successfully",
        )

    def reboot_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)

        updated_vm = vm.model_copy(update={"status": "ACTIVE"})
        self._vms[vm_id] = updated_vm

        return VMActionResponse(
            id=vm_id,
            action="reboot",
            status=updated_vm.status,
            message="VM rebooted successfully",
        )

    def update_metadata(
        self,
        vm_id: str,
        payload: VMMetadataUpdateRequest,
    ) -> VMResponse:
        vm = self.get_vm(vm_id)

        merged_metadata = {**vm.metadata, **payload.metadata}
        updated_vm = vm.model_copy(update={"metadata": merged_metadata})
        self._vms[vm_id] = updated_vm

        return updated_vm

    def delete_vm(self, vm_id: str) -> VMActionResponse:
        self.get_vm(vm_id)
        del self._vms[vm_id]

        return VMActionResponse(
            id=vm_id,
            action="delete",
            status="DELETED",
            message="VM deleted successfully",
        )