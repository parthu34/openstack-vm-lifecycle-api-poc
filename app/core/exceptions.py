from typing import Any


class AppException(Exception):
    def __init__(
        self,
        *,
        code: str,
        message: str,
        status_code: int,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


class VMNotFoundError(AppException):
    def __init__(self, vm_id: str) -> None:
        super().__init__(
            code="vm_not_found",
            message=f"VM '{vm_id}' was not found",
            status_code=404,
            details={"vm_id": vm_id},
        )


class InvalidVMStateError(AppException):
    def __init__(self, vm_id: str, current_status: str, action: str) -> None:
        super().__init__(
            code="invalid_vm_state",
            message=(
                f"Cannot perform action '{action}' when VM '{vm_id}' "
                f"is in status '{current_status}'"
            ),
            status_code=409,
            details={
                "vm_id": vm_id,
                "current_status": current_status,
                "action": action,
            },
        )


class ProviderConfigurationError(AppException):
    def __init__(self, provider_mode: str) -> None:
        super().__init__(
            code="provider_configuration_error",
            message=f"Unsupported provider mode '{provider_mode}'",
            status_code=500,
            details={"provider_mode": provider_mode},
        )