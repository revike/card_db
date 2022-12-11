import calendar
import datetime


def add_months(source_date: datetime, months: int):
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(
        year, month, day, source_date.hour, source_date.minute,
        source_date.second)
