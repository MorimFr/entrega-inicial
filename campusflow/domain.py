"""Entidades e tipos do domínio, sem dependência do framework web."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ReservationStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Room:
    id: str
    name: str
    capacity: int


@dataclass(frozen=True, slots=True)
class Reservation:
    id: str
    room_id: str
    user_id: str
    starts_at: datetime
    ends_at: datetime
    attendees: int
    status: ReservationStatus = ReservationStatus.ACTIVE

