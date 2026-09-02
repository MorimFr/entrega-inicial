from datetime import UTC, datetime, timedelta

import pytest

from campusflow.domain import ReservationStatus
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
from campusflow.service import ReservationService

START = datetime(2026, 9, 10, 10, tzinfo=UTC)


def create(
    service: ReservationService,
    *,
    room_id: str = "large",
    user_id: str = "aluno-1",
    starts_at: datetime = START,
    ends_at: datetime = START + timedelta(hours=1),
    attendees: int = 2,
):
    return service.create_reservation(
        room_id=room_id,
        user_id=user_id,
        starts_at=starts_at,
        ends_at=ends_at,
        attendees=attendees,
    )


@pytest.mark.unit
def test_creates_valid_reservation(service: ReservationService) -> None:
    reservation = create(service)

    assert reservation.id
    assert reservation.status == ReservationStatus.ACTIVE
    assert service.get_reservation(reservation.id) == reservation


@pytest.mark.unit
def test_rejects_unknown_room(service: ReservationService) -> None:
    with pytest.raises(RoomNotFoundError):
        create(service, room_id="missing")


@pytest.mark.unit
@pytest.mark.parametrize(
    ("starts_at", "ends_at"),
    [
        (START, START),
        (START, START - timedelta(minutes=1)),
        (START.replace(tzinfo=None), (START + timedelta(hours=1)).replace(tzinfo=None)),
    ],
)
def test_rejects_invalid_periods(
    service: ReservationService, starts_at: datetime, ends_at: datetime
) -> None:
    with pytest.raises(InvalidPeriodError):
        create(service, starts_at=starts_at, ends_at=ends_at)


@pytest.mark.unit
def test_accepts_exactly_two_hours(service: ReservationService) -> None:
    reservation = create(service, ends_at=START + timedelta(hours=2))

    assert reservation.ends_at - reservation.starts_at == timedelta(hours=2)


@pytest.mark.unit
def test_rejects_more_than_two_hours(service: ReservationService) -> None:
    with pytest.raises(DurationLimitError):
        create(service, ends_at=START + timedelta(hours=2, seconds=1))


@pytest.mark.unit
def test_rejects_attendees_over_capacity(service: ReservationService) -> None:
    with pytest.raises(RoomCapacityError):
        create(service, room_id="small", attendees=3)


@pytest.mark.unit
@pytest.mark.parametrize(
    ("starts_at", "ends_at"),
    [
        (START - timedelta(minutes=30), START + timedelta(minutes=30)),
        (START + timedelta(minutes=30), START + timedelta(hours=2)),
        (START + timedelta(minutes=15), START + timedelta(minutes=45)),
    ],
)
def test_rejects_overlapping_reservations(
    service: ReservationService, starts_at: datetime, ends_at: datetime
) -> None:
    create(service)

    with pytest.raises(ReservationConflictError):
        create(service, user_id="aluno-2", starts_at=starts_at, ends_at=ends_at)


@pytest.mark.unit
def test_allows_adjacent_reservations(service: ReservationService) -> None:
    first = create(service)
    second = create(
        service,
        user_id="aluno-2",
        starts_at=first.ends_at,
        ends_at=first.ends_at + timedelta(hours=1),
    )

    assert second.starts_at == first.ends_at


@pytest.mark.unit
def test_rejects_third_active_reservation_for_user_on_same_day(
    service: ReservationService,
) -> None:
    create(service, room_id="small", starts_at=START, ends_at=START + timedelta(minutes=30))
    create(
        service,
        room_id="large",
        starts_at=START + timedelta(hours=1),
        ends_at=START + timedelta(hours=2),
    )

    with pytest.raises(DailyLimitError):
        create(
            service,
            starts_at=START + timedelta(hours=3),
            ends_at=START + timedelta(hours=4),
        )


@pytest.mark.unit
def test_cancelled_reservation_releases_slot_and_daily_limit(
    service: ReservationService,
) -> None:
    first = create(service)
    create(
        service,
        starts_at=START + timedelta(hours=2),
        ends_at=START + timedelta(hours=3),
    )

    cancelled = service.cancel_reservation(first.id)
    replacement = create(service, user_id="aluno-1")

    assert cancelled.status == ReservationStatus.CANCELLED
    assert replacement.status == ReservationStatus.ACTIVE


@pytest.mark.unit
def test_rejects_cancelling_same_reservation_twice(service: ReservationService) -> None:
    reservation = create(service)
    service.cancel_reservation(reservation.id)

    with pytest.raises(AlreadyCancelledError):
        service.cancel_reservation(reservation.id)


@pytest.mark.unit
def test_rejects_getting_unknown_reservation(service: ReservationService) -> None:
    with pytest.raises(ReservationNotFoundError):
        service.get_reservation("missing")


@pytest.mark.unit
def test_availability_reflects_active_and_cancelled_reservations(
    service: ReservationService,
) -> None:
    reservation = create(service)

    assert not service.room_is_available(
        room_id="large", starts_at=START, ends_at=START + timedelta(minutes=15)
    )
    service.cancel_reservation(reservation.id)
    assert service.room_is_available(
        room_id="large", starts_at=START, ends_at=START + timedelta(minutes=15)
    )


@pytest.mark.unit
def test_availability_rejects_unknown_room_and_invalid_period(
    service: ReservationService,
) -> None:
    with pytest.raises(RoomNotFoundError):
        service.room_is_available(
            room_id="missing", starts_at=START, ends_at=START + timedelta(hours=1)
        )
    with pytest.raises(InvalidPeriodError):
        service.room_is_available(room_id="large", starts_at=START, ends_at=START)
