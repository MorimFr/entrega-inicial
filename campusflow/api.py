"""Adaptador HTTP FastAPI."""

from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Request, status
from fastapi.responses import JSONResponse

from campusflow.errors import (
    AlreadyCancelledError,
    DailyLimitError,
    DomainError,
    DurationLimitError,
    InvalidPeriodError,
    ReservationConflictError,
    ReservationNotFoundError,
    RoomCapacityError,
    RoomNotFoundError,
)
from campusflow.repository import InMemoryReservationRepository
from campusflow.schemas import (
    AvailabilityResponse,
    ErrorResponse,
    ReservationCreate,
    ReservationResponse,
    RoomResponse,
)
from campusflow.service import ReservationService


def create_app(repository: InMemoryReservationRepository | None = None) -> FastAPI:
    app = FastAPI(
        title="CampusFlow API",
        version="0.1.0",
        description="API de reserva de salas de estudo orientada por especificação.",
    )
    service = ReservationService(repository or InMemoryReservationRepository())

    def get_service() -> ReservationService:
        return service

    @app.exception_handler(DomainError)
    async def domain_error_handler(_request: Request, error: DomainError) -> JSONResponse:
        conflict_errors = (
            AlreadyCancelledError,
            DailyLimitError,
            ReservationConflictError,
        )
        not_found_errors = (ReservationNotFoundError, RoomNotFoundError)
        if isinstance(error, not_found_errors):
            http_status = status.HTTP_404_NOT_FOUND
        elif isinstance(error, conflict_errors):
            http_status = status.HTTP_409_CONFLICT
        elif isinstance(error, DurationLimitError | InvalidPeriodError | RoomCapacityError):
            http_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:  # pragma: no cover - proteção para futuros erros do domínio
            http_status = status.HTTP_400_BAD_REQUEST
        return JSONResponse(
            status_code=http_status,
            content={"code": error.code, "message": str(error)},
        )

    @app.get("/health", tags=["operational"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/rooms", response_model=list[RoomResponse], tags=["rooms"])
    def list_rooms(
        current_service: Annotated[ReservationService, Depends(get_service)],
    ) -> list[RoomResponse]:
        return [RoomResponse.model_validate(room) for room in current_service.list_rooms()]

    @app.post(
        "/reservations",
        response_model=ReservationResponse,
        status_code=status.HTTP_201_CREATED,
        responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
        tags=["reservations"],
    )
    def create_reservation(
        payload: ReservationCreate,
        current_service: Annotated[ReservationService, Depends(get_service)],
    ) -> ReservationResponse:
        reservation = current_service.create_reservation(**payload.model_dump())
        return ReservationResponse.model_validate(reservation)

    @app.get(
        "/reservations/{reservation_id}",
        response_model=ReservationResponse,
        responses={404: {"model": ErrorResponse}},
        tags=["reservations"],
    )
    def get_reservation(
        reservation_id: str,
        current_service: Annotated[ReservationService, Depends(get_service)],
    ) -> ReservationResponse:
        return ReservationResponse.model_validate(
            current_service.get_reservation(reservation_id)
        )

    @app.delete(
        "/reservations/{reservation_id}",
        response_model=ReservationResponse,
        responses={404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}},
        tags=["reservations"],
    )
    def cancel_reservation(
        reservation_id: str,
        current_service: Annotated[ReservationService, Depends(get_service)],
    ) -> ReservationResponse:
        return ReservationResponse.model_validate(
            current_service.cancel_reservation(reservation_id)
        )

    @app.get(
        "/rooms/{room_id}/availability",
        response_model=AvailabilityResponse,
        responses={404: {"model": ErrorResponse}, 422: {"model": ErrorResponse}},
        tags=["rooms"],
    )
    def check_availability(
        room_id: str,
        starts_at: Annotated[datetime, Query()],
        ends_at: Annotated[datetime, Query()],
        current_service: Annotated[ReservationService, Depends(get_service)],
    ) -> AvailabilityResponse:
        available = current_service.room_is_available(
            room_id=room_id, starts_at=starts_at, ends_at=ends_at
        )
        return AvailabilityResponse(
            room_id=room_id,
            starts_at=starts_at,
            ends_at=ends_at,
            available=available,
        )

    return app


app = create_app()
