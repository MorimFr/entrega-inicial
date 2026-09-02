"""Porta de persistência e adaptador em memória para testes isolados."""

from dataclasses import replace
from datetime import date
from typing import Protocol

from campusflow.domain import Reservation, ReservationStatus, Room


class ReservationRepository(Protocol):
    def list_rooms(self) -> list[Room]: ...

    def get_room(self, room_id: str) -> Room | None: ...

    def save(self, reservation: Reservation) -> Reservation: ...

    def get(self, reservation_id: str) -> Reservation | None: ...

    def list_for_user(
        self, user_id: str, status: ReservationStatus | None = None
    ) -> list[Reservation]: ...

    def list_active_for_room(self, room_id: str) -> list[Reservation]: ...

    def count_active_for_user_on_date(self, user_id: str, target_date: date) -> int: ...

    def cancel(self, reservation_id: str) -> Reservation | None: ...


class InMemoryReservationRepository:
    def __init__(self, rooms: list[Room] | None = None) -> None:
        self._rooms = {
            room.id: room
            for room in (
                rooms
                or [
                    Room(id="sala-a", name="Sala A", capacity=4),
                    Room(id="sala-b", name="Sala B", capacity=8),
                ]
            )
        }
        self._reservations: dict[str, Reservation] = {}

    def list_rooms(self) -> list[Room]:
        return list(self._rooms.values())

    def get_room(self, room_id: str) -> Room | None:
        return self._rooms.get(room_id)

    def save(self, reservation: Reservation) -> Reservation:
        self._reservations[reservation.id] = reservation
        return reservation

    def get(self, reservation_id: str) -> Reservation | None:
        return self._reservations.get(reservation_id)

    def list_for_user(
        self, user_id: str, status: ReservationStatus | None = None
    ) -> list[Reservation]:
        return sorted(
            (
                reservation
                for reservation in self._reservations.values()
                if reservation.user_id == user_id
                and (status is None or reservation.status == status)
            ),
            key=lambda reservation: (reservation.starts_at, reservation.id),
        )

    def list_active_for_room(self, room_id: str) -> list[Reservation]:
        return [
            reservation
            for reservation in self._reservations.values()
            if reservation.room_id == room_id
            and reservation.status == ReservationStatus.ACTIVE
        ]

    def count_active_for_user_on_date(self, user_id: str, target_date: date) -> int:
        return sum(
            reservation.user_id == user_id
            and reservation.starts_at.date() == target_date
            and reservation.status == ReservationStatus.ACTIVE
            for reservation in self._reservations.values()
        )

    def cancel(self, reservation_id: str) -> Reservation | None:
        reservation = self.get(reservation_id)
        if reservation is None:
            return None
        cancelled = replace(reservation, status=ReservationStatus.CANCELLED)
        self._reservations[reservation_id] = cancelled
        return cancelled
