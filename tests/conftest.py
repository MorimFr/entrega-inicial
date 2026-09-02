from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from campusflow.api import create_app
from campusflow.domain import Room
from campusflow.repository import InMemoryReservationRepository
from campusflow.service import ReservationService


@pytest.fixture
def repository() -> InMemoryReservationRepository:
    return InMemoryReservationRepository(
        [
            Room(id="small", name="Sala Pequena", capacity=2),
            Room(id="large", name="Sala Grande", capacity=10),
        ]
    )


@pytest.fixture
def service(repository: InMemoryReservationRepository) -> ReservationService:
    return ReservationService(repository)


@pytest.fixture
def client(repository: InMemoryReservationRepository) -> Iterator[TestClient]:
    with TestClient(create_app(repository)) as test_client:
        yield test_client

