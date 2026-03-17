from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.vms import router as vms_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Proof-of-concept API for OpenStack VM lifecycle management.",
)

app.include_router(health_router)
app.include_router(vms_router)