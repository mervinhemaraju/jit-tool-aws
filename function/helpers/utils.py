from datetime import datetime, timedelta


def calculate_end_datetime(
    start_datetime: datetime, duration_in_hours: int
) -> datetime:
    return (start_datetime + timedelta(hours=duration_in_hours)).replace(tzinfo=None)
