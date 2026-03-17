from app.core.exceptions import InvalidVMStateError, VMNotFoundError
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.providers.base import VMProvider


class VMService:
    def __init__(self, provider: VMProvider) -> None:
        self.provider = provider

    def create_vm(self, payload: VMCreateRequest) -> VMResponse:
        return self.provider.create_vm(payload)

    def list_vms(self) -> VMListResponse:
        return self.provider.list_vms()

    def get_vm(self, vm_id: str) -> VMResponse:
        try:
            return self.provider.get_vm(vm_id)
        except KeyError as exc:
            raise VMNotFoundError(vm_id) from exc

    def start_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "ACTIVE":
            raise InvalidVMStateError(vm_id, vm.status, "start")
        return self.provider.start_vm(vm_id)

    def stop_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "SHUTOFF":
            raise InvalidVMStateError(vm_id, vm.status, "stop")
        return self.provider.stop_vm(vm_id)

    def reboot_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "SHUTOFF":
            raise InvalidVMStateError(vm_id, vm.status, "reboot")
        return self.provider.reboot_vm(vm_id)

    def update_metadata(
        self,
        vm_id: str,
        payload: VMMetadataUpdateRequest,
    ) -> VMResponse:
        self.get_vm(vm_id)
        return self.provider.update_metadata(vm_id, payload)

    def delete_vm(self, vm_id: str) -> VMActionResponse:
        self.get_vm(vm_id)
        return self.provider.delete_vm(vm_id)