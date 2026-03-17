from pydantic import BaseModel, Field


class VMCreateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="VM name")
    image: str = Field(..., min_length=1, description="Image name or ID")
    flavor: str = Field(..., min_length=1, description="Flavor name or ID")
    network: str = Field(..., min_length=1, description="Network name or ID")
    key_name: str | None = Field(
        default=None,
        description="Optional SSH key pair name",
    )
    metadata: dict[str, str] = Field(
        default_factory=dict,
        description="Custom VM metadata key/value pairs",
    )
    user_data: str | None = Field(
        default=None,
        description="Optional cloud-init or startup script",
    )


class VMMetadataUpdateRequest(BaseModel):
    metadata: dict[str, str] = Field(
        ...,
        description="Metadata entries to add or update",
    )