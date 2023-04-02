import re

def is_valid_time(time):
    pattern = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
    return pattern.match(time)

def is_valid_date(date):
    pattern = re.compile(r"(0?[1-9]|[12][0-9]|3[01])\.[0-9]+\.[0-9]+", re.IGNORECASE)
    return pattern.match(date)