from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpenStack VM Lifecycle API"
    app_version: str = "0.1.0"
    environment: str = "dev"
    provider_mode: str = "mock"

    openstack_cloud: str | None = None
    openstack_region_name: str | None = None
    openstack_api_timeout: int = 30
    openstack_wait_timeout: int = 120
    openstack_verify: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()