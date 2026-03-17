from typing import Any

import openstack

from app.core.config import Settings
from app.core.exceptions import (
    CloudOperationError,
    CloudResourceLookupError,
    VMNotFoundError,
)
from app.models.vm_requests import VMCreateRequest, VMMetadataUpdateRequest
from app.models.vm_responses import VMActionResponse, VMListResponse, VMResponse
from app.providers.base import VMProvider


class RealOpenStackProvider(VMProvider):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._conn: Any | None = None

    def _get_connection(self) -> Any:
        if self._conn is None:
            connect_kwargs: dict[str, Any] = {
                "api_timeout": self.settings.openstack_api_timeout,
                "verify": self.settings.openstack_verify,
            }

            if self.settings.openstack_cloud:
                connect_kwargs["cloud"] = self.settings.openstack_cloud

            if self.settings.openstack_region_name:
                connect_kwargs["region_name"] = self.settings.openstack_region_name

            try:
                self._conn = openstack.connect(**connect_kwargs)
            except Exception as exc:
                raise CloudOperationError(
                    "connect",
                    details={"reason": str(exc)},
                ) from exc

        return self._conn

    def _extract_ref(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, dict):
            return str(value.get("name") or value.get("id") or "")
        return str(value)

    def _extract_network(self, server: Any) -> str:
        addresses = getattr(server, "addresses", None)
        if isinstance(addresses, dict) and addresses:
            return str(next(iter(addresses.keys())))
        return ""

    def _to_vm_response(self, server: Any) -> VMResponse:
        return VMResponse(
            id=str(server.id),
            name=str(getattr(server, "name", "")),
            status=str(getattr(server, "status", "")),
            image=self._extract_ref(getattr(server, "image", None)),
            flavor=self._extract_ref(getattr(server, "flavor", None)),
            network=self._extract_network(server),
            key_name=getattr(server, "key_name", None),
            metadata=getattr(server, "metadata", {}) or {},
        )

    def _require_server(self, vm_id: str) -> Any:
        conn = self._get_connection()
        server = conn.compute.find_server(vm_id, ignore_missing=True)
        if server is None:
            raise VMNotFoundError(vm_id)
        return server

    def create_vm(self, payload: VMCreateRequest) -> VMResponse:
        conn = self._get_connection()

        try:
            image = conn.image.find_image(payload.image)
            if image is None:
                raise CloudResourceLookupError("image", payload.image)

            flavor = conn.compute.find_flavor(payload.flavor)
            if flavor is None:
                raise CloudResourceLookupError("flavor", payload.flavor)

            network = conn.network.find_network(payload.network)
            if network is None:
                raise CloudResourceLookupError("network", payload.network)

            create_attrs: dict[str, Any] = {
                "name": payload.name,
                "image_id": image.id,
                "flavor_id": flavor.id,
                "networks": [{"uuid": network.id}],
                "metadata": payload.metadata,
            }

            if payload.key_name:
                create_attrs["key_name"] = payload.key_name

            if payload.user_data:
                create_attrs["user_data"] = payload.user_data

            server = conn.compute.create_server(**create_attrs)
            server = conn.compute.wait_for_server(
                server,
                status="ACTIVE",
                wait=self.settings.openstack_wait_timeout,
            )
            return self._to_vm_response(server)

        except (CloudResourceLookupError, VMNotFoundError):
            raise
        except Exception as exc:
            raise CloudOperationError(
                "create_vm",
                details={"reason": str(exc)},
            ) from exc

    def list_vms(self) -> VMListResponse:
        conn = self._get_connection()

        try:
            items = [self._to_vm_response(server) for server in conn.compute.servers()]
            return VMListResponse(items=items, count=len(items))
        except Exception as exc:
            raise CloudOperationError(
                "list_vms",
                details={"reason": str(exc)},
            ) from exc

    def get_vm(self, vm_id: str) -> VMResponse:
        try:
            server = self._require_server(vm_id)
            return self._to_vm_response(server)
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "get_vm",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc

    def start_vm(self, vm_id: str) -> VMActionResponse:
        conn = self._get_connection()

        try:
            server = self._require_server(vm_id)
            conn.compute.start_server(server)
            updated_server = conn.compute.wait_for_server(
                conn.compute.get_server(vm_id),
                status="ACTIVE",
                wait=self.settings.openstack_wait_timeout,
            )
            return VMActionResponse(
                id=vm_id,
                action="start",
                status=str(updated_server.status),
                message="VM started successfully",
            )
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "start_vm",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc

    def stop_vm(self, vm_id: str) -> VMActionResponse:
        conn = self._get_connection()

        try:
            server = self._require_server(vm_id)
            conn.compute.stop_server(server)
            updated_server = conn.compute.wait_for_server(
                conn.compute.get_server(vm_id),
                status="SHUTOFF",
                wait=self.settings.openstack_wait_timeout,
            )
            return VMActionResponse(
                id=vm_id,
                action="stop",
                status=str(updated_server.status),
                message="VM stopped successfully",
            )
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "stop_vm",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc

    def reboot_vm(self, vm_id: str) -> VMActionResponse:
        conn = self._get_connection()

        try:
            server = self._require_server(vm_id)
            conn.compute.reboot_server(server, reboot_type="SOFT")
            updated_server = conn.compute.wait_for_server(
                conn.compute.get_server(vm_id),
                status="ACTIVE",
                wait=self.settings.openstack_wait_timeout,
            )
            return VMActionResponse(
                id=vm_id,
                action="reboot",
                status=str(updated_server.status),
                message="VM rebooted successfully",
            )
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "reboot_vm",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc

    def update_metadata(
        self,
        vm_id: str,
        payload: VMMetadataUpdateRequest,
    ) -> VMResponse:
        conn = self._get_connection()

        try:
            self._require_server(vm_id)
            conn.compute.set_server_metadata(vm_id, **payload.metadata)
            updated_server = conn.compute.get_server(vm_id)
            return self._to_vm_response(updated_server)
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "update_metadata",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc

    def delete_vm(self, vm_id: str) -> VMActionResponse:
        conn = self._get_connection()

        try:
            self._require_server(vm_id)
            conn.compute.delete_server(vm_id, ignore_missing=False)
            return VMActionResponse(
                id=vm_id,
                action="delete",
                status="DELETED",
                message="VM deleted successfully",
            )
        except VMNotFoundError:
            raise
        except Exception as exc:
            raise CloudOperationError(
                "delete_vm",
                details={"vm_id": vm_id, "reason": str(exc)},
            ) from exc