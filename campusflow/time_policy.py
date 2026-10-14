"""Política de calendário do campus (UTC-03 fixo nesta entrega)."""

from datetime import date, datetime, timedelta, timezone

CAMPUS_TIMEZONE = timezone(timedelta(hours=-3))


def campus_date(instant: datetime) -> date:
    return instant.astimezone(CAMPUS_TIMEZONE).date()
