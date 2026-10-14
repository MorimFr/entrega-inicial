"""Regressões da homologação final: RN-03, RN-06 e RN-10."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path
from threading import Barrier

import pytest
from fastapi.testclient import TestClient

from campusflow.domain import Room
from campusflow.errors import (
    AlreadyCancelledError,
    DailyLimitError,
    InvalidAttendeeCountError,
    ReservationConflictError,
)
from campusflow.repository import InMemoryReservationRepository
from campusflow.service import ReservationService
from campusflow.sqlite_repository import SQLiteReservationRepository


@pytest.fixture(params=["memory", "sqlite"])
def persistent_service(request: pytest.FixtureRequest, tmp_path: Path) -> ReservationService:
    rooms = [Room("room", "Sala de teste", 10)]
    repository = (
        InMemoryReservationRepository(rooms)
        if request.param == "memory"
        else SQLiteReservationRepository(tmp_path / "regression.db", rooms)
    )
    return ReservationService(repository)


def reserve(service: ReservationService, instant: str, attendees: object = 1):
    starts_at = datetime.fromisoformat(instant)
    return service.create_reservation(
        room_id="room",
        user_id="test-user",
        starts_at=starts_at,
        ends_at=starts_at + timedelta(minutes=30),
        attendees=attendees,
    )


@pytest.mark.parametrize("attendees", [True, 1.5, "2"])
def test_domain_requires_real_integer(persistent_service, attendees):
    with pytest.raises(InvalidAttendeeCountError):
        reserve(persistent_service, "2026-10-20T10:00:00+00:00", attendees)


def test_listing_orders_instants_not_iso_strings(persistent_service):
    # 08:00-03:00 = 11:00Z; 10:00Z é o primeiro instante.
    later = reserve(persistent_service, "2026-10-20T08:00:00-03:00")
    earlier = reserve(persistent_service, "2026-10-20T10:00:00+00:00")
    assert [r.id for r in persistent_service.list_reservations(user_id="test-user")] == [
        earlier.id,
        later.id,
    ]


def test_daily_limit_uses_campus_day_not_client_offset(persistent_service):
    # Os três instantes são 20/10 em UTC-03, embora dois estejam escritos como 21/10Z.
    reserve(persistent_service, "2026-10-20T20:00:00-03:00")
    reserve(persistent_service, "2026-10-21T00:00:00+00:00")
    with pytest.raises(DailyLimitError):
        reserve(persistent_service, "2026-10-21T01:00:00+00:00")


@pytest.mark.parametrize("attendees", [True, 1.0, "2"])
def test_http_does_not_coerce_attendee_type(client: TestClient, attendees):
    response = client.post(
        "/reservations",
        json={
            "room_id": "large",
            "user_id": "test-user",
            "starts_at": "2026-10-20T10:00:00Z",
            "ends_at": "2026-10-20T11:00:00Z",
            "attendees": attendees,
        },
    )
    assert response.status_code == 422


def test_concurrent_creation_preserves_room_invariant(persistent_service):
    gate = Barrier(6)

    def attempt(index):
        gate.wait(timeout=10)
        try:
            starts_at = datetime.fromisoformat("2026-10-22T10:00:00+00:00")
            persistent_service.create_reservation(
                room_id="room",
                user_id=f"user-{index}",
                starts_at=starts_at,
                ends_at=starts_at + timedelta(minutes=30),
                attendees=1,
            )
            return "created"
        except ReservationConflictError:
            return "conflict"

    with ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(attempt, range(6)))
    assert results.count("created") == 1
    assert results.count("conflict") == 5


def test_concurrent_creation_preserves_daily_limit(persistent_service):
    gate = Barrier(4)

    def attempt(index):
        gate.wait(timeout=10)
        try:
            reserve(persistent_service, f"2026-10-22T{10 + index}:00:00+00:00")
            return "created"
        except DailyLimitError:
            return "daily_limit"

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(attempt, range(4)))
    assert results.count("created") == 2
    assert results.count("daily_limit") == 2


def test_concurrent_cancellation_has_one_transition(persistent_service):
    created = reserve(persistent_service, "2026-10-22T10:00:00+00:00")
    gate = Barrier(4)

    def attempt(_index):
        gate.wait(timeout=10)
        try:
            persistent_service.cancel_reservation(created.id)
            return "cancelled"
        except AlreadyCancelledError:
            return "already_cancelled"

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(attempt, range(4)))
    assert results.count("cancelled") == 1
    assert results.count("already_cancelled") == 3


def test_sqlite_transaction_rolls_back_and_can_recover(tmp_path: Path):
    repository = SQLiteReservationRepository(tmp_path / "rollback.db", [Room("room", "R", 4)])
    service = ReservationService(repository)
    with pytest.raises(RuntimeError, match="simulated failure"):
        with repository.transaction():
            # Gravação direta testa o contrato de rollback do adaptador.
            from campusflow.domain import Reservation

            starts_at = datetime.fromisoformat("2026-10-22T10:00:00+00:00")
            repository.save(
                Reservation(
                    id="rolled-back",
                    room_id="room",
                    user_id="test-user",
                    starts_at=starts_at,
                    ends_at=starts_at + timedelta(minutes=30),
                    attendees=1,
                )
            )
            raise RuntimeError("simulated failure")
    assert repository.get("rolled-back") is None
    assert reserve(service, "2026-10-22T10:00:00+00:00").id


def test_independent_sqlite_instances_share_atomic_boundary(tmp_path: Path):
    path = tmp_path / "shared.db"
    services = [
        ReservationService(SQLiteReservationRepository(path, [Room("room", "R", 4)]))
        for _ in range(4)
    ]
    gate = Barrier(4)

    def attempt(index):
        gate.wait(timeout=10)
        try:
            reserve(services[index], "2026-10-22T10:00:00+00:00")
            return "created"
        except ReservationConflictError:
            return "conflict"

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(attempt, range(4)))
    assert results.count("created") == 1
    assert results.count("conflict") == 3
