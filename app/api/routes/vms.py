from fastapi import APIRouter, HTTPException, status

from app.models.common import ErrorResponse
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse

router = APIRouter(prefix="/api/v1/vms", tags=["vms"])


@router.post(
    "",
    response_model=VMResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def create_vm(payload: VMCreateRequest) -> VMResponse:
    return VMResponse(
        id="mock-vm-001",
        name=payload.name,
        status="BUILD",
        image=payload.image,
        flavor=payload.flavor,
        network=payload.network,
        key_name=payload.key_name,
        metadata=payload.metadata,
    )


@router.get(
    "",
    response_model=VMListResponse,
    responses={500: {"model": ErrorResponse}},
)
def list_vms() -> VMListResponse:
    return VMListResponse(items=[], count=0)


@router.get(
    "/{vm_id}",
    response_model=VMResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def get_vm(vm_id: str) -> VMResponse:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"VM '{vm_id}' was not found",
    )


@router.post(
    "/{vm_id}/start",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def start_vm(vm_id: str) -> VMActionResponse:
    return VMActionResponse(
        id=vm_id,
        action="start",
        status="ACTIVE",
        message="VM start requested successfully",
    )


@router.post(
    "/{vm_id}/stop",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def stop_vm(vm_id: str) -> VMActionResponse:
    return VMActionResponse(
        id=vm_id,
        action="stop",
        status="SHUTOFF",
        message="VM stop requested successfully",
    )


@router.post(
    "/{vm_id}/reboot",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def reboot_vm(vm_id: str) -> VMActionResponse:
    return VMActionResponse(
        id=vm_id,
        action="reboot",
        status="REBOOT",
        message="VM reboot requested successfully",
    )


@router.patch(
    "/{vm_id}/metadata",
    response_model=VMResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def update_vm_metadata(vm_id: str, payload: VMMetadataUpdateRequest) -> VMResponse:
    return VMResponse(
        id=vm_id,
        name="placeholder-vm",
        status="ACTIVE",
        image="ubuntu-22.04",
        flavor="m1.small",
        network="private-net",
        key_name="default-key",
        metadata=payload.metadata,
    )


@router.delete(
    "/{vm_id}",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def delete_vm(vm_id: str) -> VMActionResponse:
    return VMActionResponse(
        id=vm_id,
        action="delete",
        status="DELETED",
        message="VM delete requested successfully",
    )