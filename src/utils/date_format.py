# Toggles date string between "dd.mm.yy" and "yy.mm.dd"
def format_date_string(date: str):
    values = date.split(".")
    return values[2] + "." + values[1] + "." + values[0]
