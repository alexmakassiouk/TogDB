import sqlite3
from datetime import datetime

con = sqlite3.connect("src/tog.db")
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
    combined_date_time = date + " " + time
    try:
        dt = datetime.strptime(combined_date_time, '%d.%m.%y %H:%M')
    except ValueError:
        print("Invalid date!")
        return
    weekday = dt.isoweekday()

    sql = f"""
        SELECT t.ID, t.startstasjon, t.avgangstid, ts.jernbanestasjonNavn, ts.avgangstid, t.endestasjon, t.ankomsttid, tu.ukedagID
        FROM togrute AS t INNER JOIN togrute_stoppestasjon AS ts ON (t.ID = ts.togruteID)
        INNER JOIN togrute_ukedager AS tu ON (tu.togruteID = t.ID)
        WHERE ((tu.ukedagID = {weekday}) OR tu.ukedagID = {weekday+1})
        AND (ts.jernbanestasjonNavn = '{dep}' OR ts.jernbanestasjonNavn = '{des}')
        ORDER BY tu.ukedagID, t.ID, ts.avgangstid
    """
    rows = []
    for row in cur.execute(sql):
        rows.append(row)
        print(row)
    

construct_query("Fauske", "Bodø", "29.03.23", "07:00")