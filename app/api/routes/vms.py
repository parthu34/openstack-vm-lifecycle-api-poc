from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_provider
from app.models.common import ErrorResponse
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.providers.base import VMProvider

router = APIRouter(prefix="/api/v1/vms", tags=["vms"])


ProviderDependency = Annotated[VMProvider, Depends(get_provider)]


def _raise_vm_not_found(vm_id: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"VM '{vm_id}' was not found",
    )


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
    provider: ProviderDependency,
) -> VMResponse:
    return provider.create_vm(payload)


@router.get(
    "",
    response_model=VMListResponse,
    responses={500: {"model": ErrorResponse}},
)
def list_vms(provider: ProviderDependency) -> VMListResponse:
    return provider.list_vms()


@router.get(
    "/{vm_id}",
    response_model=VMResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def get_vm(vm_id: str, provider: ProviderDependency) -> VMResponse:
    try:
        return provider.get_vm(vm_id)
    except KeyError:
        _raise_vm_not_found(vm_id)


@router.post(
    "/{vm_id}/start",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def start_vm(vm_id: str, provider: ProviderDependency) -> VMActionResponse:
    try:
        return provider.start_vm(vm_id)
    except KeyError:
        _raise_vm_not_found(vm_id)


@router.post(
    "/{vm_id}/stop",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def stop_vm(vm_id: str, provider: ProviderDependency) -> VMActionResponse:
    try:
        return provider.stop_vm(vm_id)
    except KeyError:
        _raise_vm_not_found(vm_id)


@router.post(
    "/{vm_id}/reboot",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def reboot_vm(vm_id: str, provider: ProviderDependency) -> VMActionResponse:
    try:
        return provider.reboot_vm(vm_id)
    except KeyError:
        _raise_vm_not_found(vm_id)


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
    provider: ProviderDependency,
) -> VMResponse:
    try:
        return provider.update_metadata(vm_id, payload)
    except KeyError:
        _raise_vm_not_found(vm_id)


@router.delete(
    "/{vm_id}",
    response_model=VMActionResponse,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
def delete_vm(vm_id: str, provider: ProviderDependency) -> VMActionResponse:
    try:
        return provider.delete_vm(vm_id)
    except KeyError:
        _raise_vm_not_found(vm_id)