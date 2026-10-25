"""Contratos públicos de entrada e saída da API."""

from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from campusflow.domain import ReservationStatus


def require_iso_datetime(value: object) -> str:
    """Impede a coerção silenciosa de epoch para uma data ISO do contrato HTTP."""
    if not isinstance(value, str) or "T" not in value.upper():
        raise ValueError("Use data ISO 8601 com separador T e fuso horário.")
    return value


ISODateTime = Annotated[datetime, BeforeValidator(require_iso_datetime)]


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    capacity: int


class ReservationCreate(BaseModel):
    room_id: str = Field(min_length=1, max_length=50)
    user_id: str = Field(min_length=1, max_length=100)
    starts_at: ISODateTime
    ends_at: ISODateTime
    attendees: int = Field(ge=1, strict=True)


class ReservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    room_id: str
    user_id: str
    starts_at: datetime
    ends_at: datetime
    attendees: int
    status: ReservationStatus


class AvailabilityResponse(BaseModel):
    room_id: str
    starts_at: datetime
    ends_at: datetime
    available: bool


class ErrorResponse(BaseModel):
    code: str
    message: str


class ValidationErrorResponse(BaseModel):
    detail: list[dict[str, Any]]
