"""Erros de domínio traduzidos para respostas HTTP na camada de API."""


class DomainError(Exception):
    code = "domain_error"


class RoomNotFoundError(DomainError):
    code = "room_not_found"


class ReservationNotFoundError(DomainError):
    code = "reservation_not_found"


class InvalidPeriodError(DomainError):
    code = "invalid_period"


class DurationLimitError(DomainError):
    code = "duration_limit_exceeded"


class RoomCapacityError(DomainError):
    code = "room_capacity_exceeded"


class ReservationConflictError(DomainError):
    code = "reservation_conflict"


class DailyLimitError(DomainError):
    code = "daily_limit_exceeded"


class AlreadyCancelledError(DomainError):
    code = "already_cancelled"

