import sqlite3
from search import construct_query
from datetime import datetime

con = sqlite3.connect("tog.db")
cur = con.cursor()

def find_tickets_main():
    emails = []
    for row in cur.execute("SELECT epost FROM kunde"):
        emails.append(row[0])

    email = " "
    email = input("What is your email? ")
    while email not in emails:
        print("No such email. Make sure you are registered and entered the correct email")
        email = input("Try again or write 'exit' to go back to menu ")
        if email == "exit":
            return
    

    departure = input("Where are you departing from? ")
    destination = input("Where are you going? ")
    date = input("Which date are you travelling? (dd.mm.yy) ")
    time = input("At which time do you want to travel? (hh:mm) ")

    trainroutes_two_days, weekday, new_date, next_date = construct_query(departure, destination, date, time)
    
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
    
    trainrouteID = int(trainroutes[int(index_ans)-1][0])
    print()

    customerID = cur.execute("SELECT k.kundenummer FROM kunde AS k WHERE k.epost = ?", [str(email)]).fetchone()[0]
    today = datetime.now()
    current_date = today.strftime("%d.%m.%Y")[0:-4] + today.strftime("%d.%m.%Y")[-2:]
    current_time = today.strftime("%H:%M")
    formatted_purchase_time = current_date +" " + current_time
    new_order_sql = f"""
    INSERT INTO kundeordre(kjopstidspunkt, kundenummer, togruteID, reisedato)
    VALUES (?, ?, ?, ?)
    """
    cur.execute(new_order_sql, (formatted_purchase_time, customerID, trainrouteID, date))
    con.commit()
    order_ID = cur.execute("SELECT ordrenummer FROM kundeordre WHERE kundenummer = ? AND kjopstidspunkt = ?", (customerID, formatted_purchase_time)).fetchone()[0]

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
    for row in carriage_data:
        if 'sove' in row[2]:
            bed_route = True
    bed_ticket = False
    if bed_route:
        bed_ans = input("Would you like a bed or seat for this travel? (b/s)")
        if bed_ans.lower() == 'b':
            bed_ticket = True
    
    if bed_ticket:
        carriage_ID = 4
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
            carriage_ID = 5

    if bed_ticket:
        print("Here are the available beds:")
        available_beds = [str(bed) for bed in get_available_beds(trainrouteID, date, customerID)]
        for bed in available_beds:
            if int(bed) % 2 == 1:
                if str(int(bed)+1) in available_beds:
                    print(bed + " " + str(int(bed)+1))
                else:
                    print(bed)
            else:
                if str(int(bed)-1) not in available_beds:
                    print("  " + bed)
        # print(available_beds)
            
        requested_bed = " "
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

def get_available_beds(trainrouteID, date, customerID):

    get_beds_sql = f"""
    SELECT
        k.kundenummer, k.ordrenummer, b.ID, b.vognID, b.plassnummer
    FROM
        kundeordre AS k 
    INNER JOIN 
        billett AS b 
    ON 
        (k.ordrenummer = b.ordrenummer)
    WHERE
        k.togruteID = ?
    AND
        k.reisedato = ?
    """
    res = cur.execute(get_beds_sql, (trainrouteID, date))
    trainroute_bed_data = res.fetchall()
    carriage_bed_numbers = [1,2,3,4,5,6,7,8]
    for row in trainroute_bed_data:
        # Remove occupied beds from list of all bed numbers
        carriage_bed_numbers.remove(row[4])
        # Don't show available beds in already occupied cabin if different customer than the occupied cabin
        if customerID != row[0]:
            if row[4] % 2 == 0:
                if (row[4]-1) in carriage_bed_numbers:
                    carriage_bed_numbers.remove(row[4]-1)
            elif row[4] % 2 == 1:
                if (row[4]+1) in carriage_bed_numbers:
                    carriage_bed_numbers.remove(row[4]+1)
    return carriage_bed_numbers

def test():
    
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
    trainrouteID = 3
    carriage_data = cur.execute(get_carriage_data_sql, [trainrouteID]).fetchall()
    print(carriage_data)
    for row in carriage_data:
        if 'sove' in row[2]:
            print("sovevogn!")
# test()
# def get_available_spots(trainrouteID, date):


# find_tickets_main()