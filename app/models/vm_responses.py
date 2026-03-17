from pydantic import BaseModel, Field


class VMResponse(BaseModel):
    id: str = Field(..., description="VM unique identifier")
    name: str = Field(..., description="VM display name")
    status: str = Field(..., description="Current VM status")
    image: str = Field(..., description="Image used by the VM")
    flavor: str = Field(..., description="Flavor used by the VM")
    network: str = Field(..., description="Network attached to the VM")
    key_name: str | None = Field(default=None, description="SSH key pair name")
    metadata: dict[str, str] = Field(default_factory=dict)


class VMActionResponse(BaseModel):
    id: str = Field(..., description="VM unique identifier")
    action: str = Field(..., description="Lifecycle action performed")
    status: str = Field(..., description="Updated VM status")
    message: str = Field(..., description="Result summary message")


class VMListResponse(BaseModel):
    items: list[VMResponse]
    count: int