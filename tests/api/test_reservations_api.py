from fastapi.testclient import TestClient


def valid_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "room_id": "large",
        "user_id": "aluno-1",
        "starts_at": "2026-09-10T10:00:00Z",
        "ends_at": "2026-09-10T11:00:00Z",
        "attendees": 4,
    }
    payload.update(overrides)
    return payload


def test_health_check(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lists_rooms(client: TestClient) -> None:
    response = client.get("/rooms")

    assert response.status_code == 200
    assert response.json() == [
        {"id": "small", "name": "Sala Pequena", "capacity": 2},
        {"id": "large", "name": "Sala Grande", "capacity": 10},
    ]


def test_create_then_get_reservation(client: TestClient) -> None:
    created = client.post("/reservations", json=valid_payload())

    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "active"
    assert body["room_id"] == "large"

    fetched = client.get(f"/reservations/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_returns_structured_domain_error(client: TestClient) -> None:
    response = client.post(
        "/reservations", json=valid_payload(room_id="small", attendees=3)
    )

    assert response.status_code == 422
    assert response.json() == {
        "code": "room_capacity_exceeded",
        "message": "Quantidade de participantes excede a capacidade da sala.",
    }


def test_returns_validation_error_for_invalid_input(client: TestClient) -> None:
    response = client.post("/reservations", json=valid_payload(attendees=0))

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][-1] == "attendees"


def test_conflict_and_availability_contract(client: TestClient) -> None:
    assert client.post("/reservations", json=valid_payload()).status_code == 201

    conflict = client.post(
        "/reservations",
        json=valid_payload(
            user_id="aluno-2",
            starts_at="2026-09-10T10:30:00Z",
            ends_at="2026-09-10T11:30:00Z",
        ),
    )
    availability = client.get(
        "/rooms/large/availability",
        params={
            "starts_at": "2026-09-10T10:30:00Z",
            "ends_at": "2026-09-10T11:00:00Z",
        },
    )

    assert conflict.status_code == 409
    assert conflict.json()["code"] == "reservation_conflict"
    assert availability.status_code == 200
    assert availability.json()["available"] is False


def test_cancel_contract(client: TestClient) -> None:
    created = client.post("/reservations", json=valid_payload()).json()

    cancelled = client.delete(f"/reservations/{created['id']}")
    repeated = client.delete(f"/reservations/{created['id']}")

    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert repeated.status_code == 409
    assert repeated.json()["code"] == "already_cancelled"


def test_unknown_resources_return_404(client: TestClient) -> None:
    reservation = client.get("/reservations/missing")
    room = client.get(
        "/rooms/missing/availability",
        params={
            "starts_at": "2026-09-10T10:00:00Z",
            "ends_at": "2026-09-10T11:00:00Z",
        },
    )

    assert reservation.status_code == 404
    assert reservation.json()["code"] == "reservation_not_found"
    assert room.status_code == 404
    assert room.json()["code"] == "room_not_found"

