from typing import Any

from pydantic import BaseModel, Field


class ApiError(BaseModel):
    code: str
    message: str
    field: str | None = None


class ApiResponse(BaseModel):
    data: Any = None
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[ApiError] = Field(default_factory=list)


def success_response(data: Any, meta: dict[str, Any] | None = None) -> ApiResponse:
    return ApiResponse(data=data, meta=meta or {}, errors=[])
