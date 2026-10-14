"""Regressões da homologação final: RN-03, RN-06 e RN-10."""

from datetime import datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from campusflow.domain import Room
from campusflow.errors import DailyLimitError, InvalidAttendeeCountError
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
        room_id="room", user_id="test-user", starts_at=starts_at,
        ends_at=starts_at + timedelta(minutes=30), attendees=attendees,
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
        earlier.id, later.id,
    ]


def test_daily_limit_uses_campus_day_not_client_offset(persistent_service):
    # Os três instantes são 20/10 em UTC-03, embora dois estejam escritos como 21/10Z.
    reserve(persistent_service, "2026-10-20T20:00:00-03:00")
    reserve(persistent_service, "2026-10-21T00:00:00+00:00")
    with pytest.raises(DailyLimitError):
        reserve(persistent_service, "2026-10-21T01:00:00+00:00")


@pytest.mark.parametrize("attendees", [True, 1.0, "2"])
def test_http_does_not_coerce_attendee_type(client: TestClient, attendees):
    response = client.post("/reservations", json={
        "room_id": "large", "user_id": "test-user",
        "starts_at": "2026-10-20T10:00:00Z", "ends_at": "2026-10-20T11:00:00Z",
        "attendees": attendees,
    })
    assert response.status_code == 422
