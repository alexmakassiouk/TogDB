import sqlite3
from datetime import datetime

con = sqlite3.connect("tog.db")
cur = con.cursor()

def search_main():
    departure = input("Where are you departing from? ")
    destination = input("Where are you going? ")
    date = input("Which date are you travelling? (dd.mm.yy) ")
    time = input("At which time do you want to travel? (hh:mm) ")
    print()

def construct_query(dep, des, date: str, time: str):
    day, month, year = date.split(".")
    hour, minute = time.split(":")
    dt = datetime.combine(datetime.date(datetime.year(int(year)), datetime.month(int(month)), datetime.day(int(day))), datetime.time(datetime.hour(int(hour)), datetime.minute(int(minute))))
    weekday = dt.isoweekday()

    sql = f"""
    SELECT tu.togruteID, ts.jernbanestasjonNavn, ts.avgangstid, t.endestasjon, t.ankomsttid
        FROM togrute_ukedager AS tu
        INNER JOIN togrute AS t ON (tu.togruteID = t.ID)
        INNER JOIN togrute_stoppestasjon AS ts ON (t.ID = ts.togruteID)
        WHERE tu.ukedagID = {weekday}
        AND ts.jernbanestasjonNavn = '{dep}'
    """

    for row in cur.execute(sql):
        print(row)

construct_query("Steinkjer", "Bodø", "29.03.23", "07:00")