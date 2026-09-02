"""Contratos públicos de entrada e saída da API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from campusflow.domain import ReservationStatus


class RoomResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    capacity: int


class ReservationCreate(BaseModel):
    room_id: str = Field(min_length=1, max_length=50)
    user_id: str = Field(min_length=1, max_length=100)
    starts_at: datetime
    ends_at: datetime
    attendees: int = Field(ge=1)


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

