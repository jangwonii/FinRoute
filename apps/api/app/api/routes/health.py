from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.envelope import ApiResponse, success_response
from app.schemas.health import HealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiResponse)
def health_check() -> ApiResponse:
    settings = get_settings()
    payload = HealthStatus(
        status="ok",
        service=settings.app_name,
        environment=settings.environment,
        database_configured=bool(settings.database_url),
    )
    return success_response(payload.model_dump())
