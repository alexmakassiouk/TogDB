import sqlite3
from datetime import datetime
from utils.date_format import format_date_string

con = sqlite3.connect("tog.db")
cur = con.cursor()

def search_main():
    departure = input("Where are you departing from? ")
    destination = input("Where are you going? ")
    date = input("Which date are you travelling? (dd.mm.yy) ")
    time = input("At which time do you want to travel? (hh:mm) ")
    print()
    results, weekday, new_date, next_date = construct_query(departure, destination, format_date_string(date), time)
    print_searched_routes(results, weekday, format_date_string(new_date), format_date_string(next_date))


def construct_query(dep, des, date: str, time: str):
    combined_date_time = date + " " + time
    # Catch invalid format on date and time
    try:
        dt = datetime.strptime(combined_date_time, '%y.%m.%d %H:%M')
    except ValueError:
        print("Invalid date!")
        return
    
    # Get the value which is used as ukedagID in the DB
    weekday = dt.isoweekday()

    date = str(dt.year) + "." + str(dt.month) + "." + str(dt.day)
    next_date = str(dt.year) + "." + str(dt.month) + "." + str(dt.day+1)

    # Get rows for each stop station for each train route for the two days after the inputted time where dep or des station is included in the row. Include start and stop station on train route in each row
    sql = f"""
        SELECT 
          t.ID, t.startstasjon, t.avgangstid, ts.jernbanestasjonNavn, ts.avgangstid, t.endestasjon, t.ankomsttid, tu.ukedagID
        FROM 
          togrute AS t 
          INNER JOIN togrute_stoppestasjon AS ts ON (t.ID = ts.togruteID)
          INNER JOIN togrute_ukedager AS tu ON (tu.togruteID = t.ID)
        WHERE 
          (((tu.ukedagID = ? AND t.avgangstid >= ?) OR tu.ukedagID = ?) OR (tu.ukedagID = ? AND ts.avgangstid >= ?) OR tu.ukedagID = ?)
          AND (ts.jernbanestasjonNavn = ? OR ts.jernbanestasjonNavn = ? OR t.startstasjon = ? OR t.endestasjon = ?)
        ORDER BY tu.ukedagID, t.ID, ts.avgangstid
    """
    rows = []
    # If weekday = 7 then it will also check for weekday = 1, since this is the weekday after 7
    for row in cur.execute(sql, (weekday, time, (weekday%7)+1, weekday, time, (weekday%7)+1, dep, des, dep, des)):
        rows.append(row)

    matching_trainroutes = []

    for row in rows:
        # If departure is from a starting station and destination is at a stop
        if row[1] == dep and row[3] == des:
            # If train has not left yet that day or the day is the next one. Taking new week into account
            if row[2] > time or row[7] == (weekday+1)%7:
                matching_trainroutes.append((row[0], row[1], row[2], row[3], row[4], row[7]))
        #If departure is from a stop and destination is at an end station
        elif row[3] == dep and row[5] == des:
            # If train has not left yet that day or the day is the next one
            if row[4] > time or row[7] == (weekday+1)%7:
                matching_trainroutes.append((row[0], row[3], row[4], row[5], row[6], row[7]))
        # If departure is from a starting station and destination is at an end station
        elif row[1] == dep and row[5] == des:
            # Avoid duplicates. This list will contain matching trainroutes which has same trainroute ID and same weekdayID as current row
            already_exists = [trainroute for trainroute in matching_trainroutes if trainroute[0] == row[0] and trainroute[5]==row[7]]
            # If list is empty: Trainroute in current row has not yet been added to matching trainroutes
            if len(already_exists) == 0:
                # If train has not left yet that day
                if row[2] > time:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))
                # If train is on the next day
                elif row[7] == (weekday+1)%7:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))
                #Bug handling if weekday is saturday
                elif row[7] == weekday+1:
                    matching_trainroutes.append((row[0], row[1], row[2], row[5], row[6], row[7]))

    # This for loop adds trainroutes when both departure and destination are stops along the trainroute.
    for i in range(1,len(rows)):
        # If two rows are the same trainroute and the former row is departure stop and current row is destination stop -> Match
        if rows[i-1][0] == rows[i][0] and rows[i-1][3] == dep and rows[i][3] == des and rows[i-1][7] == rows[i][7]:
            # If train has not left yet or train is on the next day
            if rows[i-1][4] >= time or rows[i-1][7] != weekday:
                matching_trainroutes.append((rows[i-1][0], rows[i-1][3], rows[i-1][4], rows[i][3], rows[i][4], rows[i][7]))
    
    # Sort results on date
    matching_trainroutes.sort(key= lambda t: (t[5]%7))
    return matching_trainroutes, weekday, date, next_date

def print_searched_routes(matching_trainroutes: list, weekday: int, date: str, next_date: str):
    print("Here are some suggested train routes:")
    for trainroute in matching_trainroutes:
        if trainroute[5] == weekday:
            print("Linje " + str(trainroute[0]) + ": " + date +" "+ str(trainroute[1]) + " kl. " + str(trainroute[2]) + " - " + str(trainroute[3]) + " kl. " + str(trainroute[4]))
        else:
            print("Linje " + str(trainroute[0]) + ": " + next_date +" "+ str(trainroute[1]) + " kl. " + str(trainroute[2]) + " - " + str(trainroute[3]) + " kl. " + str(trainroute[4]))
    print()
