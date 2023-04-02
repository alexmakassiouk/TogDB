import sqlite3
from search import construct_query
from datetime import datetime
from utils.date_format import format_date_string

con = sqlite3.connect("tog.db")
cur = con.cursor()

def find_tickets_main():
    emails = []
    # Get all registered emails in DB
    for row in cur.execute("SELECT epost FROM kunde"):
        emails.append(row[0])

    email = " "
    email = input("What is your email? ")
    # Only allow registered users to purchase tickets
    while email not in emails:
        print("No such email. Make sure you are registered and entered the correct email")
        email = input("Try again or write 'exit' to go back to menu ")
        if email == "exit":
            return
    

    departure = input("Where are you departing from? ")
    destination = input("Where are you going? ")
    date = input("Which date are you travelling? (dd.mm.yy) ")
    time = input("At which time do you want to travel? (hh:mm) ")

    # Search for train routes on the requested date and the next one. Reuse search code
    trainroutes_two_days, weekday, new_date, next_date = construct_query(departure, destination, format_date_string(date), time)
    
    # Show only trainroutes on requested date
    trainroutes = list(filter(lambda t: t[5] == weekday, trainroutes_two_days))
    
    print("Here are the routes on this day.")
    for route in trainroutes:
        print(str(trainroutes.index(route)+1) + ". " + "Linje " + str(route[0]) + ": " + date +" "+ str(route[1]) + " kl. " + str(route[2]) + " - " + str(route[3]) + " kl. " + str(route[4]))
    if len(trainroutes) == 0:
        print("No routes matches your search!")
        return
    elif len(trainroutes) == 1:
        ans = input("Would You like to purchase tickets on this route? (y/n)")
        if ans == "y":
            index_ans = 0
        else:
            return
    else:
        index_ans = input("Which one would you like to purchase tickets on? ")
    
    # When user answers 1 or 2 this correlates to index 0 or 1 in the trainroutes list
    trainrouteID = int(trainroutes[int(index_ans)-1][0])
    print()

    customerID = cur.execute("SELECT k.kundenummer FROM kunde AS k WHERE k.epost = ?", [str(email)]).fetchone()[0]
    today = datetime.now()
    current_date = today.strftime("%y.%m.%d")
    current_time = today.strftime("%H:%M")
    formatted_purchase_time = current_date +" " + current_time

    new_order_sql = f"""
    INSERT INTO kundeordre(kjopstidspunkt, kundenummer, togruteID, reisedato)
    VALUES (?, ?, ?, ?)
    """

    # Create new order in DB
    cur.execute(new_order_sql, (formatted_purchase_time, customerID, trainrouteID, format_date_string(date)))
    con.commit()
    # Retrieve assigned order number in DB. Ticket will be assigned this number
    order_ID = cur.execute("SELECT ordrenummer FROM kundeordre WHERE kundenummer = ? AND kjopstidspunkt = ?", (customerID, formatted_purchase_time)).fetchone()[0]

    # Find which carriages are available for customer on this travel
    get_carriage_data_sql = f"""
    SELECT 
        tvo.vognID, tvo.nummer_fra_front, vt.navn
    FROM
        togrute_vogn_oppsett AS tvo 
        INNER JOIN 
          vogn AS v ON (tvo.vognID = v.ID) 
        INNER JOIN 
          vogntype AS vt ON (v.vogntypeNavn = vt.navn)
    WHERE
        tvo.togruteID = ?"""
    carriage_data = cur.execute(get_carriage_data_sql, [trainrouteID]).fetchall()
    bed_route = False
    # Check to see if beds are available on this train
    for row in carriage_data:
        if 'sove' in row[2]:
            bed_route = True
    bed_ticket = False
    if bed_route:
        bed_ans = input("Would you like a bed or seat for this travel? (b/s)")
        if bed_ans.lower() == 'b':
            bed_ticket = True
    
    # Since only one carriage with beds, assign the carriage_ID in DB. Another approach if project should be scalable
    if bed_ticket:
        carriage_ID = 4
    # Only one carriage which is on a trainroute with beds but has seats itself. Another approach if project should be scalable
    elif bed_route:
        carriage_ID = 3
    else:
        if len(carriage_data)>1:
            print("Here are the carriages to choose from:")
            print("1. Sittevogn")
            print("2. Sittevogn")
            carriage_ans = input("Which carriage would you like to sit in? (1/2) ")
            carriage_ID = int(carriage_ans)
            if carriage_ID != 1 and carriage_ID !=2:
                print("Invalid input!")
                return
        else:
            # If train only has one carriage then it is trainroute with ID=3. Carriage 5 is the carriage on that train rotue. Would use another approach if project should be scalable
            carriage_ID = 5

    # If customer wants bed: Simpler constraints. Cabin is reserved for the whole train trip
    if bed_ticket:
        print("Here are the available beds:")
        available_beds = [str(bed) for bed in get_available_beds(trainrouteID, format_date_string(date), customerID)]
        # Display cabins and bed nicely for user 
        for bed in available_beds:
            if int(bed) % 2 == 1:
                if str(int(bed)+1) in available_beds:
                    print(bed + " " + str(int(bed)+1))
                else:
                    print(bed)
            else:
                if str(int(bed)-1) not in available_beds:
                    print("  " + bed)
            
        requested_bed = " "
        # While input is not compliant to constraints
        while requested_bed not in available_beds:
            requested_bed = input("Which bed would you like? ")
            if requested_bed == "exit":
                return
            elif requested_bed in available_beds:
                purchase_bed_sql = f"""
                    INSERT INTO 
                        billett(plassnummer, pastigning, avstigning, ordrenummer, vognID)
                    VALUES
                        (?, ?, ?, ?, ?)
                """
                cur.execute(purchase_bed_sql, (int(requested_bed), departure, destination, order_ID, carriage_ID))
                con.commit()
                print("Success!", "You have bought bed number " + requested_bed + " in carriage number 2 for " + departure + " - " + destination + " for Linje " + str(trainroutes.index(route)+1) + " on " + date)
            else:
                print("Not available, please try again or type 'exit'")
    
    # If customer wants seat. Seats can belong to multiple customers if customers trips on the same train route are not overlapping.
    else:
        print("Here are the available seats for your trip:")
        available_seats_print = ""
        # All available seats for given train on given date for given carriage and given departure- and destination station
        available_seats = get_available_seats(trainrouteID, format_date_string(date), carriage_ID, departure, destination)
        # Nice seat display for user with rows and seats
        for i in range(12):
            if i%4 == 0:
                available_seats_print +=" \n"
            if i%2 == 0 and i%4 != 0:
                available_seats_print += "  "
            if i+1 in available_seats:
                available_seats_print += " " + str(i+1)
            else:
                available_seats_print += "  "
        print(available_seats_print)
        # While input is not compliant to constraints
        while True:
            requested_seat = input("Please select your seat number: ")
            if requested_seat == "exit":
                return
            try:
                requested_seat = int(requested_seat)
                if requested_seat not in available_seats:
                    print("Not available!")
                else:
                    break
            except:
                print("Please enter a number!")
        # Insert new ticket for requested seat
        purchase_seat_sql = """
            INSERT INTO
                billett(plassnummer, pastigning, avstigning, ordrenummer, vognID)
            VALUES
                (?, ?, ?, ?, ?)
        """
        cur.execute(purchase_seat_sql, (requested_seat, departure, destination, order_ID, carriage_ID))
        con.commit()
        print("Success! You have bought seat number " + str(requested_seat) + " in carriage number " + str(carriage_ID) + " for " + departure + " - " + destination + " for Linje " + str(trainroutes.index(route)+1) + " on " + date)

# Return list of all available beds for given trainroute on a given date and a customer. A customer cannot buy a bed ticket in the same cabin as another customer
def get_available_beds(trainrouteID, date, customerID):

    get_beds_sql = f"""
    SELECT
        k.kundenummer, k.ordrenummer, b.ID, b.vognID, b.plassnummer
    FROM
        kundeordre AS k 
        INNER JOIN 
          billett AS b ON (k.ordrenummer = b.ordrenummer)
    WHERE
        k.togruteID = ?
        AND
        k.reisedato = ?
    """
    res = cur.execute(get_beds_sql, (trainrouteID, date))
    trainroute_bed_data = res.fetchall()
    # All bed numbers in a bed carriage
    carriage_bed_numbers = [1,2,3,4,5,6,7,8]
    for row in trainroute_bed_data:
        # Remove occupied beds from list of all bed numbers
        if row[4] in carriage_bed_numbers:
            carriage_bed_numbers.remove(row[4])
        # Don't show available beds in already occupied cabin if different customer than the occupied cabin
        if customerID != row[0]:
            #1/2, 3/4 and so on are beds in the same cabin. A customer cannot buy ticket to bed in same cabin as another customer
            # If even bed number
            if row[4] % 2 == 0:
                if (row[4]-1) in carriage_bed_numbers:
                    carriage_bed_numbers.remove(row[4]-1)
            # If odd bed number
            elif row[4] % 2 == 1:
                if (row[4]+1) in carriage_bed_numbers:
                    carriage_bed_numbers.remove(row[4]+1)
    return carriage_bed_numbers


# Return a list of all available seats for given trainroute on a given date for a given carriage and given departure/destination station
def get_available_seats(trainrouteID, date, carriageID, dep, des):
    # Not very scaleable because of the project's scope. No more than 6 stations. Would use Common Table Expression if scalability was required
    # Table will contain all relevant tickets and all stations after the tickets departure station
    get_taken_seats_sql = """
    SELECT 
        b.ID AS billettID, b.plassnummer, b.pastigning, b.avstigning, k.togruteID, k.reisedato, b.vognID, d.stasjon1, d.stasjon2, d2.stasjon2, d3.stasjon2, d4.stasjon2, d5.stasjon2
    FROM 
        billett b 
        INNER JOIN delstrekning d ON (b.pastigning = d.stasjon1)
        INNER JOIN kundeordre k ON (b.ordrenummer = k.ordrenummer)
        LEFT JOIN delstrekning d2 ON (d2.stasjon1 = d.stasjon2)
        LEFT JOIN delstrekning d3 ON (d2.stasjon2 = d3.stasjon1)
        LEFT JOIN delstrekning d4 ON (d3.stasjon2 = d4.stasjon1)
        LEFT JOIN delstrekning d5 ON (d4.stasjon2 = d5.stasjon1)
    WHERE
        k.togruteID = ?
        AND k.reisedato = ?
        AND b.vognID = ?
    ORDER BY
        b.ID, d.stasjon1
    """
    res = cur.execute(get_taken_seats_sql, (trainrouteID, date, carriageID))
    taken_seats_data = res.fetchall()

    # Get data for the stations that customer will travel through
    get_customer_stations_sql = """
    SELECT 
        d.stasjon2, d2.stasjon2, d3.stasjon2, d4.stasjon2, d5.stasjon2
    FROM
        delstrekning d
        LEFT JOIN delstrekning d2 ON (d.stasjon2 = d2.stasjon1)
        LEFT JOIN delstrekning d3 ON (d2.stasjon2 = d3.stasjon1)
        LEFT JOIN delstrekning d4 ON (d3.stasjon2 = d4.stasjon1)
        LEFT JOIN delstrekning d5 ON (d4.stasjon2 = d5.stasjon1)
    WHERE
        d.stasjon1 = ?
    ORDER BY
        d.stasjon2
    """
    res = cur.execute(get_customer_stations_sql, [dep])
    # Include departure station
    customer_stations_data_raw = (dep, *res.fetchone())
    customer_stations_data = []

    # Refine data to not include stations after the requested destination
    for station in customer_stations_data_raw:
        customer_stations_data.append(station)
        if station == des:
            break

    # All seat numbers in a carriage with seats
    all_seat_numbers = [i for i in range(1, 13)]
    # 2D Table with a ticket on each row and seat number in first column
    seat_taken_distances = [[taken_seats_data[i][1]] for i in range(len(taken_seats_data))]
    for i in range(len(taken_seats_data)):
        # Append first distance on which the seat number is occupied
        seat_taken_distances[i].append(taken_seats_data[i][7])
        for j in range(8,len(taken_seats_data[i])):
            # If ticket on multiple distances: Append all distances to that seat
            seat_taken_distances[i].append(taken_seats_data[i][j])
            # If destination, append no more
            if taken_seats_data[i][j] == taken_seats_data[i][3]:
                break
    
    # Remove taken seats from all seat numbers
    for row in seat_taken_distances:
        # Check if customers departure station is in another's ticket and it is not the other's destination station.
        # Check if customers destination station is in another's ticket and it it not the other s departure station
        # Check if another customer's both departure and destination is in requested distance
        # Check that seat has not already been removed from the available seats
        if ((dep in row and row[-1] != dep) or (des in row and row[1] != des) or (row[1] in customer_stations_data and row[-1] in customer_stations_data)) and row[0] in all_seat_numbers:
            all_seat_numbers.remove(row[0])
    return all_seat_numbers

