"""Adaptador SQLite persistente para a porta de reservas."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import replace
from datetime import date, datetime
from pathlib import Path

from campusflow.domain import Reservation, ReservationStatus, Room

DEFAULT_ROOMS = [
    Room(id="sala-a", name="Sala A", capacity=4),
    Room(id="sala-b", name="Sala B", capacity=8),
]


class SQLiteReservationRepository:
    """Persistência local sem dependências externas, compatível com a porta do domínio."""

    def __init__(
        self, database_path: str | Path, rooms: list[Room] | None = None
    ) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize(rooms or DEFAULT_ROOMS)

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path, timeout=5)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self, rooms: list[Room]) -> None:
        with self._connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    capacity INTEGER NOT NULL CHECK (capacity > 0)
                );
                CREATE TABLE IF NOT EXISTS reservations (
                    id TEXT PRIMARY KEY,
                    room_id TEXT NOT NULL REFERENCES rooms(id),
                    user_id TEXT NOT NULL,
                    starts_at TEXT NOT NULL,
                    ends_at TEXT NOT NULL,
                    attendees INTEGER NOT NULL CHECK (attendees > 0),
                    status TEXT NOT NULL CHECK (status IN ('active', 'cancelled'))
                );
                CREATE INDEX IF NOT EXISTS idx_reservations_room_status
                    ON reservations(room_id, status, starts_at);
                CREATE INDEX IF NOT EXISTS idx_reservations_user_status
                    ON reservations(user_id, status, starts_at);
                """
            )
            connection.executemany(
                "INSERT OR IGNORE INTO rooms(id, name, capacity) VALUES (?, ?, ?)",
                [(room.id, room.name, room.capacity) for room in rooms],
            )

    @staticmethod
    def _reservation_from_row(row: sqlite3.Row) -> Reservation:
        return Reservation(
            id=row["id"],
            room_id=row["room_id"],
            user_id=row["user_id"],
            starts_at=datetime.fromisoformat(row["starts_at"]),
            ends_at=datetime.fromisoformat(row["ends_at"]),
            attendees=row["attendees"],
            status=ReservationStatus(row["status"]),
        )

    def list_rooms(self) -> list[Room]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT id, name, capacity FROM rooms ORDER BY id"
            ).fetchall()
        return [Room(id=row["id"], name=row["name"], capacity=row["capacity"]) for row in rows]

    def get_room(self, room_id: str) -> Room | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT id, name, capacity FROM rooms WHERE id = ?", (room_id,)
            ).fetchone()
        if row is None:
            return None
        return Room(id=row["id"], name=row["name"], capacity=row["capacity"])

    def save(self, reservation: Reservation) -> Reservation:
        with self._connection() as connection:
            connection.execute(
                """
                INSERT INTO reservations(
                    id, room_id, user_id, starts_at, ends_at, attendees, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    reservation.id,
                    reservation.room_id,
                    reservation.user_id,
                    reservation.starts_at.isoformat(),
                    reservation.ends_at.isoformat(),
                    reservation.attendees,
                    reservation.status.value,
                ),
            )
        return reservation

    def get(self, reservation_id: str) -> Reservation | None:
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM reservations WHERE id = ?", (reservation_id,)
            ).fetchone()
        return None if row is None else self._reservation_from_row(row)

    def list_for_user(
        self, user_id: str, status: ReservationStatus | None = None
    ) -> list[Reservation]:
        query = "SELECT * FROM reservations WHERE user_id = ?"
        parameters: list[str] = [user_id]
        if status is not None:
            query += " AND status = ?"
            parameters.append(status.value)
        query += " ORDER BY starts_at, id"
        with self._connection() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._reservation_from_row(row) for row in rows]

    def list_active_for_room(self, room_id: str) -> list[Reservation]:
        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT * FROM reservations
                WHERE room_id = ? AND status = 'active'
                ORDER BY starts_at, id
                """,
                (room_id,),
            ).fetchall()
        return [self._reservation_from_row(row) for row in rows]

    def count_active_for_user_on_date(self, user_id: str, target_date: date) -> int:
        return sum(
            reservation.starts_at.date() == target_date
            for reservation in self.list_for_user(user_id, ReservationStatus.ACTIVE)
        )

    def cancel(self, reservation_id: str) -> Reservation | None:
        reservation = self.get(reservation_id)
        if reservation is None:
            return None
        cancelled = replace(reservation, status=ReservationStatus.CANCELLED)
        with self._connection() as connection:
            connection.execute(
                "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
                (reservation_id,),
            )
        return cancelled
