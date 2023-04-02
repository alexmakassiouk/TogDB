def format_date_string(date: str):
    # Changes between "dd.mm.yy" and "yy.mm.dd"
    values = date.split(".")
    return values[2] + "." + values[1] + "." + values[0]
