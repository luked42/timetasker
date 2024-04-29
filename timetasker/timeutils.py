import re
from datetime import timedelta


def parse_duration(interval: str) -> timedelta:
    m = re.match(r"(?:(?P<hours>\d+)h)?(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?", interval)
    hours = int(m.group("hours")) if m.group("hours") else 0
    minutes = int(m.group("minutes")) if m.group("minutes") else 0
    seconds = int(m.group("seconds")) if m.group("seconds") else 0
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)
