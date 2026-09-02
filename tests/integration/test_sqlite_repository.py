from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from campusflow.api import create_app
from campusflow.domain import ReservationStatus, Room
from campusflow.service import ReservationService
from campusflow.sqlite_repository import SQLiteReservationRepository


@pytest.mark.integration
def test_persists_reservation_and_cancellation_between_instances(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "campusflow.db"
    rooms = [Room(id="persistente", name="Sala Persistente", capacity=6)]
    first_service = ReservationService(
        SQLiteReservationRepository(database_path, rooms=rooms)
    )
    starts_at = datetime(2026, 9, 15, 9, tzinfo=UTC)
    created = first_service.create_reservation(
        room_id="persistente",
        user_id="aluno-persistente",
        starts_at=starts_at,
        ends_at=starts_at + timedelta(hours=1),
        attendees=3,
    )

    restarted_service = ReservationService(SQLiteReservationRepository(database_path))
    persisted = restarted_service.get_reservation(created.id)
    cancelled = restarted_service.cancel_reservation(created.id)

    final_service = ReservationService(SQLiteReservationRepository(database_path))
    final_state = final_service.get_reservation(created.id)

    assert persisted == created
    assert cancelled.status == ReservationStatus.CANCELLED
    assert final_state.status == ReservationStatus.CANCELLED


@pytest.mark.integration
def test_sqlite_repository_supports_room_and_user_queries(tmp_path: Path) -> None:
    repository = SQLiteReservationRepository(tmp_path / "queries.db")
    service = ReservationService(repository)
    starts_at = datetime(2026, 9, 16, 10, tzinfo=UTC)
    reservation = service.create_reservation(
        room_id="sala-a",
        user_id="aluno-consulta",
        starts_at=starts_at,
        ends_at=starts_at + timedelta(minutes=30),
        attendees=2,
    )

    assert repository.get_room("ausente") is None
    assert [room.id for room in repository.list_rooms()] == ["sala-a", "sala-b"]
    assert service.list_reservations(user_id="aluno-consulta") == [reservation]
    assert not service.room_is_available(
        room_id="sala-a",
        starts_at=starts_at,
        ends_at=starts_at + timedelta(minutes=15),
    )
    assert repository.cancel("ausente") is None


@pytest.mark.integration
def test_default_api_preserves_data_after_restart(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    database_path = tmp_path / "api.db"
    monkeypatch.setenv("CAMPUSFLOW_DATABASE_PATH", str(database_path))
    payload = {
        "room_id": "sala-a",
        "user_id": "aluno-reinicio",
        "starts_at": "2026-09-17T10:00:00-03:00",
        "ends_at": "2026-09-17T11:00:00-03:00",
        "attendees": 2,
    }

    with TestClient(create_app()) as first_client:
        created = first_client.post("/reservations", json=payload)
    reservation_id = created.json()["id"]

    with TestClient(create_app()) as restarted_client:
        fetched = restarted_client.get(f"/reservations/{reservation_id}")

    assert created.status_code == 201
    assert fetched.status_code == 200
    assert fetched.json()["id"] == reservation_id
