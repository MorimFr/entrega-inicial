"""Casos de uso e regras de negócio de reservas."""

from datetime import datetime, timedelta
from uuid import uuid4

from campusflow.domain import Reservation, ReservationStatus, Room
from campusflow.errors import (
    AlreadyCancelledError,
    DailyLimitError,
    DurationLimitError,
    InvalidPeriodError,
    ReservationConflictError,
    ReservationNotFoundError,
    RoomCapacityError,
    RoomNotFoundError,
)
from campusflow.repository import ReservationRepository

MAX_DURATION = timedelta(hours=2)
MAX_DAILY_RESERVATIONS = 2


class ReservationService:
    def __init__(self, repository: ReservationRepository) -> None:
        self.repository = repository

    def list_rooms(self) -> list[Room]:
        return self.repository.list_rooms()

    def create_reservation(
        self,
        *,
        room_id: str,
        user_id: str,
        starts_at: datetime,
        ends_at: datetime,
        attendees: int,
    ) -> Reservation:
        room = self.repository.get_room(room_id)
        if room is None:
            raise RoomNotFoundError("Sala não encontrada.")
        if starts_at.tzinfo is None or ends_at.tzinfo is None or ends_at <= starts_at:
            raise InvalidPeriodError(
                "Início e fim devem ter fuso horário, e o fim deve ser posterior ao início."
            )
        if ends_at - starts_at > MAX_DURATION:
            raise DurationLimitError("A reserva não pode durar mais que 2 horas.")
        if attendees > room.capacity:
            raise RoomCapacityError("Quantidade de participantes excede a capacidade da sala.")
        if self.repository.count_active_for_user_on_date(user_id, starts_at.date()) >= 2:
            raise DailyLimitError("Cada usuário pode manter até 2 reservas ativas por dia.")

        for existing in self.repository.list_active_for_room(room_id):
            if starts_at < existing.ends_at and ends_at > existing.starts_at:
                raise ReservationConflictError("A sala já está reservada nesse intervalo.")

        reservation = Reservation(
            id=str(uuid4()),
            room_id=room_id,
            user_id=user_id,
            starts_at=starts_at,
            ends_at=ends_at,
            attendees=attendees,
        )
        return self.repository.save(reservation)

    def get_reservation(self, reservation_id: str) -> Reservation:
        reservation = self.repository.get(reservation_id)
        if reservation is None:
            raise ReservationNotFoundError("Reserva não encontrada.")
        return reservation

    def cancel_reservation(self, reservation_id: str) -> Reservation:
        reservation = self.get_reservation(reservation_id)
        if reservation.status == ReservationStatus.CANCELLED:
            raise AlreadyCancelledError("A reserva já foi cancelada.")
        cancelled = self.repository.cancel(reservation_id)
        assert cancelled is not None
        return cancelled

    def room_is_available(
        self, *, room_id: str, starts_at: datetime, ends_at: datetime
    ) -> bool:
        if self.repository.get_room(room_id) is None:
            raise RoomNotFoundError("Sala não encontrada.")
        if starts_at.tzinfo is None or ends_at.tzinfo is None or ends_at <= starts_at:
            raise InvalidPeriodError("Intervalo de consulta inválido.")
        return not any(
            starts_at < reservation.ends_at and ends_at > reservation.starts_at
            for reservation in self.repository.list_active_for_room(room_id)
        )

