from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_vm_service
from app.models.common import ErrorResponse
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.services.vm_service import VMService

router = APIRouter(prefix="/api/v1/vms", tags=["vms"])


ServiceDependency = Annotated[VMService, Depends(get_vm_service)]


@router.post(
    "",
    response_model=VMResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def create_vm(
    payload: VMCreateRequest,
    service: ServiceDependency,
) -> VMResponse:
    return service.create_vm(payload)


@router.get(
    "",
    response_model=VMListResponse,
    responses={500: {"model": ErrorResponse}},
)
def list_vms(service: ServiceDependency) -> VMListResponse:
    return service.list_vms()


@router.get(
    "/{vm_id}",
    response_model=VMResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def get_vm(vm_id: str, service: ServiceDependency) -> VMResponse:
    return service.get_vm(vm_id)


@router.post(
    "/{vm_id}/start",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def start_vm(vm_id: str, service: ServiceDependency) -> VMActionResponse:
    return service.start_vm(vm_id)


@router.post(
    "/{vm_id}/stop",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def stop_vm(vm_id: str, service: ServiceDependency) -> VMActionResponse:
    return service.stop_vm(vm_id)


@router.post(
    "/{vm_id}/reboot",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def reboot_vm(vm_id: str, service: ServiceDependency) -> VMActionResponse:
    return service.reboot_vm(vm_id)


@router.patch(
    "/{vm_id}/metadata",
    response_model=VMResponse,
    responses={
        404: {"model": ErrorResponse},
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def update_vm_metadata(
    vm_id: str,
    payload: VMMetadataUpdateRequest,
    service: ServiceDependency,
) -> VMResponse:
    return service.update_metadata(vm_id, payload)


@router.delete(
    "/{vm_id}",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def delete_vm(vm_id: str, service: ServiceDependency) -> VMActionResponse:
    return service.delete_vm(vm_id)