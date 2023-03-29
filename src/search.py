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
    construct_query(departure, destination, date, time)

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
    date = str(dt.day) + "." + str(dt.month) + "." + str(dt.year)
    next_date = str(dt.day+1) + "." + str(dt.month) + "." + str(dt.year)

    sql = f"""
        SELECT t.ID, t.startstasjon, t.avgangstid, ts.jernbanestasjonNavn, ts.avgangstid, t.endestasjon, t.ankomsttid, tu.ukedagID
        FROM togrute AS t INNER JOIN togrute_stoppestasjon AS ts ON (t.ID = ts.togruteID)
        INNER JOIN togrute_ukedager AS tu ON (tu.togruteID = t.ID)
        WHERE ((tu.ukedagID = {weekday} AND ts.avgangstid > '{time}') OR tu.ukedagID = {(weekday%7)+1})
        AND (ts.jernbanestasjonNavn = '{dep}' OR ts.jernbanestasjonNavn = '{des}' OR t.startstasjon = '{dep}' OR t.endestasjon = '{des}')
        ORDER BY tu.ukedagID, t.ID, ts.avgangstid
    """
    rows = []
    for row in cur.execute(sql):
        rows.append(row)

    matching_trainroutes = []

    for row in rows:
        # If departure is from a starting station and destination is at a stop
        if row[1] == dep and row[3] == des:
            if row[2] > time or row[7] == (weekday+1)%7:
                matching_trainroutes.append((row[0], row[1], row[2], row[3], row[4], row[7]))
        #If departure is from a stop and destination is at an end station
        elif row[3] == dep and row[5] == des:
            matching_trainroutes.append((row[0], row[3], row[4], row[5], row[6], row[7]))
        # If departure is from a starting station and destination is at an end station
        elif row[1] == dep and row[5] == des:
            # Avoid duplicates. This list will contain matching trainroutes which has same trainroute ID and same weekdayID as current row
            already_exists = [trainroute for trainroute in matching_trainroutes if trainroute[0] == row[0] and trainroute[5]==row[7]]
            # If list is empty: Trainroute in current row has not yet been added to matching trainroutes
            if len(already_exists) == 0:
                if row[2] > time:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))
                elif row[7] == (weekday+1)%7:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))
                elif row[7] == weekday+1:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))

    # This for loop adds trainroutes when both departure and destination are stops along the trainroute.
    for i in range(1,len(rows)):
        # If two rows are the same trainroute and the former row is departure stop and current row is destination stop -> Match
        if rows[i-1][0] == rows[i][0] and rows[i-1][3] == dep and rows[i][3] == des and rows[i-1][7] == rows[i][7]:
            matching_trainroutes.append((rows[i-1][0], rows[i-1][3], rows[i-1][4], rows[i][3], rows[i][4], rows[i][7]))
    
    for trainroute in matching_trainroutes:
        if trainroute[5] == weekday:
            print("Linje " + str(trainroute[0]) + ": " + date +" "+ str(trainroute[1]) + " kl. " + str(trainroute[2]) + " - " + str(trainroute[3]) + " kl. " + str(trainroute[4]))
        else:
            print("Linje " + str(trainroute[0]) + ": " + next_date +" "+ str(trainroute[1]) + " kl. " + str(trainroute[2]) + " - " + str(trainroute[3]) + " kl. " + str(trainroute[4]))
    print()
    #for row in rows:
        #print(row)

    

construct_query( "Steinkjer","Fauske", "10.04.23", "09:20")