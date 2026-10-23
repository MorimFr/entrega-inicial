"""Contratos definitivos da release 1.0.0 (Issue #26)."""

import pytest
from fastapi.testclient import TestClient

def test_openapi_exposes_stable_version_and_room_not_found(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "1.0.0"
    assert "404" in schema["paths"]["/reservations"]["post"]["responses"]


@pytest.mark.parametrize("starts_at", [1792746000, True, "1792746000"])
def test_dates_require_iso8601_not_coerced_epoch(client: TestClient, starts_at: object) -> None:
    response = client.post("/reservations", json={
        "room_id": "large", "user_id": "demo-date",
        "starts_at": starts_at, "ends_at": "2026-10-23T11:00:00Z", "attendees": 1,
    })
    assert response.status_code == 422
    assert "detail" in response.json()
