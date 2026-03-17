from abc import ABC, abstractmethod

from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse


class VMProvider(ABC):
    @abstractmethod
    def create_vm(self, payload: VMCreateRequest) -> VMResponse:
        raise NotImplementedError

    @abstractmethod
    def list_vms(self) -> VMListResponse:
        raise NotImplementedError

    @abstractmethod
    def get_vm(self, vm_id: str) -> VMResponse:
        raise NotImplementedError

    @abstractmethod
    def start_vm(self, vm_id: str) -> VMActionResponse:
        raise NotImplementedError

    @abstractmethod
    def stop_vm(self, vm_id: str) -> VMActionResponse:
        raise NotImplementedError

    @abstractmethod
    def reboot_vm(self, vm_id: str) -> VMActionResponse:
        raise NotImplementedError

    @abstractmethod
    def update_metadata(
        self,
        vm_id: str,
        payload: VMMetadataUpdateRequest,
    ) -> VMResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_vm(self, vm_id: str) -> VMActionResponse:
        raise NotImplementedError