import sqlite3

con = sqlite3.connect("tog.db")
cur = con.cursor()

def departures_main():
    station_input = input("From which station would you like to see train routes? ")

    weekday_input = input("On which weekday would you like to see departures? (1: Monday, 7: Sunday, etc.) ")
    print()
    construct_query(station_input, weekday_input)
    con.close()

def construct_query(station, weekday):

    # Query all stations along a trainroute
    sql_middle_stations = f"""
        SELECT 
          tu.togruteID, ts.jernbanestasjonNavn, ts.avgangstid, t.endestasjon, t.ankomsttid
        FROM 
          togrute_ukedager AS tu
          INNER JOIN 
            togrute AS t ON (tu.togruteID = t.ID)
          INNER JOIN 
            togrute_stoppestasjon AS ts ON (t.ID = ts.togruteID)
        WHERE 
          tu.ukedagID = ?
          AND ts.jernbanestasjonNavn = ?
        """
    
    rows = []
    for row in cur.execute(sql_middle_stations, (weekday, station)):
        # First column: 0 for start station, 1 for middle station, 2 for end station
        rows.append((1, *row))

    # Query all starting stations (Trondheim S and Mo i Rana)
    sql_start_stations = f"""
    SELECT 
      tu.togruteID, t.startstasjon, t.avgangstid, t.endestasjon, t.ankomsttid
    FROM 
      togrute_ukedager AS tu
      INNER JOIN 
        togrute AS t ON (tu.togruteID = t.ID)
    WHERE 
      tu.ukedagID = ?
      AND t.startstasjon = ?
    """
    for row in cur.execute(sql_start_stations, (weekday, station)):
        # First column: 0 for start station, 1 for middle station, 2 for end station
        rows.append((0, *row))

    # Query for all end stations (Trondheim S and Bodø)
    sql_end_stations = f"""
    SELECT 
      tu.togruteID, t.endestasjon, t.ankomsttid
    FROM 
      togrute_ukedager AS tu
      INNER JOIN 
        togrute AS t ON (tu.togruteID = t.ID)
    WHERE 
      tu.ukedagID = ?
      AND t.endestasjon = ?
    """
    for row in cur.execute(sql_end_stations, (weekday, station)):
        # First column: 0 for start station, 1 for middle station, 2 for end station
        rows.append((2, *row))

    # Nice display for user. Show all train routes at a station, even the ones that just arrive
    for row in rows:
        if row[0] == 0 or row[0] == 1:
            print("Togrute", row[1], ":", row[2], "kl.", row[3], "-", row[4], "kl.", row[5])
        elif row[0] == 2:
            print("Togrute", row[1], ": Ankommer", row[2], "kl.", row[3])

    print()
