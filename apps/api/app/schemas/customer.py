from datetime import datetime
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    birth_year: int | None = Field(default=None, ge=1900, le=2100)
    gender: str | None = Field(default=None, max_length=40)
    occupation: str | None = Field(default=None, max_length=120)
    household_type: str | None = Field(default=None, max_length=80)
    memo: str | None = Field(default=None, max_length=2000)


class CustomerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    birth_year: int | None = Field(default=None, ge=1900, le=2100)
    gender: str | None = Field(default=None, max_length=40)
    occupation: str | None = Field(default=None, max_length=120)
    household_type: str | None = Field(default=None, max_length=80)
    memo: str | None = Field(default=None, max_length=2000)

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("At least one customer field must be provided")
        return self


class CustomerRead(BaseModel):
    customer_id: UUID
    advisor_id: UUID
    name: str
    birth_year: int | None
    gender: str | None
    occupation: str | None
    household_type: str | None
    memo: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
