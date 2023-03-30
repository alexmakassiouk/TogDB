import sqlite3

# Open a connection to the database file
conn = sqlite3.connect('src/tog.db')

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Define a function to get the names of all train routes
def get_train_routes():
    cur.execute("SELECT navn FROM banestrekning")
    return [row[0] for row in cur.fetchall()]

# Define a function to get the names of all train stations
def get_train_stations():
    cur.execute("SELECT navn FROM jernbanestasjon")
    return [row[0] for row in cur.fetchall()]

# Define a function to get the elevations of all train stations
def get_train_station_elevations():
    cur.execute("SELECT navn, moh FROM jernbanestasjon")
    return dict(cur.fetchall())

# Define a function to get the lengths of all train sections
def get_train_section_lengths():
    cur.execute("SELECT stasjon1, stasjon2, lengde FROM delstrekning")
    return [row for row in cur.fetchall()]

# Define a function to get the stop stations and their order for a train route
def get_train_route_stations(route_name):
    cur.execute("SELECT s.jernbanestasjonNavn FROM banestrekning_stoppestasjoner s JOIN banestrekning b ON b.ID = s.banestrekningID WHERE b.navn = ?", (route_name,))
    return [row[0] for row in cur.fetchall()]

# Define a function to get the departure times for a train route at a particular station
def get_train_departure_times(route_name, station_name):
    cur.execute("SELECT avgangstid FROM togrute t JOIN togrute_stoppestasjon s ON t.ID = s.togruteID WHERE t.startstasjon = ? AND t.endestasjon = ? AND s.jernbanestasjonNavn = ?", (get_train_route_stations(route_name)[0], get_train_route_stations(route_name)[-1], station_name))
    return [row[0] for row in cur.fetchall()]

# Define a function to get the train route for a given start and end station
def get_train_route(start_station, end_station):
    cur.execute("SELECT navn FROM banestrekning WHERE startstasjon = ? AND endestasjon = ?", (start_station, end_station))
    return cur.fetchone()[0]

trainroute_event_data = [
    (1, "03.04.23"),
    (2, "03.04.23"),
    (3, "03.04.23"),
    (1, "04.04.23"),
    (2, "04.04.23"),
    (3, "04.04.23"),
]

def insert_trainroute_event_data(trainroute_events):
    cur.executemany("INSERT INTO togruteforekomst VALUES(?, ?)", trainroute_event_data)
    conn.commit()

def print_trainroute_event_data():
    print("Inserted data for trainroute events:")
    for row in cur.execute("SELECT * FROM togruteforekomst"):
        print(row)

insert_trainroute_event_data(trainroute_event_data)
print_trainroute_event_data()

# Close the database connection
conn.close()
