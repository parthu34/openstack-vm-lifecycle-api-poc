import logging

from app.core.exceptions import InvalidVMStateError, VMNotFoundError
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.providers.base import VMProvider

logger = logging.getLogger("app.vm_service")


class VMService:
    def __init__(self, provider: VMProvider) -> None:
        self.provider = provider

    def create_vm(self, payload: VMCreateRequest) -> VMResponse:
        logger.info(
            "create_vm_requested name=%s image=%s flavor=%s network=%s",
            payload.name,
            payload.image,
            payload.flavor,
            payload.network,
        )
        vm = self.provider.create_vm(payload)
        logger.info("create_vm_succeeded vm_id=%s status=%s", vm.id, vm.status)
        return vm

    def list_vms(self) -> VMListResponse:
        result = self.provider.list_vms()
        logger.info("list_vms_succeeded count=%s", result.count)
        return result

    def get_vm(self, vm_id: str) -> VMResponse:
        try:
            vm = self.provider.get_vm(vm_id)
            logger.info("get_vm_succeeded vm_id=%s status=%s", vm.id, vm.status)
            return vm
        except KeyError as exc:
            logger.warning("get_vm_not_found vm_id=%s", vm_id)
            raise VMNotFoundError(vm_id) from exc

    def start_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "ACTIVE":
            logger.warning(
                "start_vm_invalid_state vm_id=%s current_status=%s",
                vm_id,
                vm.status,
            )
            raise InvalidVMStateError(vm_id, vm.status, "start")

        result = self.provider.start_vm(vm_id)
        logger.info("start_vm_succeeded vm_id=%s status=%s", vm_id, result.status)
        return result

    def stop_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "SHUTOFF":
            logger.warning(
                "stop_vm_invalid_state vm_id=%s current_status=%s",
                vm_id,
                vm.status,
            )
            raise InvalidVMStateError(vm_id, vm.status, "stop")

        result = self.provider.stop_vm(vm_id)
        logger.info("stop_vm_succeeded vm_id=%s status=%s", vm_id, result.status)
        return result

    def reboot_vm(self, vm_id: str) -> VMActionResponse:
        vm = self.get_vm(vm_id)
        if vm.status == "SHUTOFF":
            logger.warning(
                "reboot_vm_invalid_state vm_id=%s current_status=%s",
                vm_id,
                vm.status,
            )
            raise InvalidVMStateError(vm_id, vm.status, "reboot")

        result = self.provider.reboot_vm(vm_id)
        logger.info("reboot_vm_succeeded vm_id=%s status=%s", vm_id, result.status)
        return result

    def update_metadata(
        self,
        vm_id: str,
        payload: VMMetadataUpdateRequest,
    ) -> VMResponse:
        self.get_vm(vm_id)
        vm = self.provider.update_metadata(vm_id, payload)
        logger.info(
            "update_metadata_succeeded vm_id=%s metadata_keys=%s",
            vm_id,
            ",".join(sorted(payload.metadata.keys())),
        )
        return vm

    def delete_vm(self, vm_id: str) -> VMActionResponse:
        self.get_vm(vm_id)
        result = self.provider.delete_vm(vm_id)
        logger.info("delete_vm_succeeded vm_id=%s", vm_id)
        return result