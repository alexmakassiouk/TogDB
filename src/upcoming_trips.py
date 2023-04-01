import sqlite3
from datetime import datetime

con = sqlite3.connect("tog.db")
cur = con.cursor()

def upcoming_trips_main():

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
    
    customer_res = cur.execute("SELECT k.kundenummer, k.navn FROM kunde AS k WHERE k.epost = ?", [str(email)]).fetchone()
    customer_ID = customer_res[0]
    customer_name = customer_res[1]
    today = datetime.now()
    current_date = today.strftime("%d.%m.%Y")[0:-4] + today.strftime("%d.%m.%Y")[-2:]

# whooops - date is stored in a non-comparable way of course... Should be yy.mm.dd 
    upcoming_trips_sql = f"""
        SELECT 
            k.ordrenummer, k.kjopstidspunkt, k.togruteID, k.reisedato, b.ID, b.vognID, b.plassnummer, b.pastigning, b.avstigning 
        FROM
            kundeordre AS k
        INNER JOIN
            billett AS b
        ON
            (k.ordrenummer = b.ordrenummer)
        WHERE
            k.kundenummer = ?
        AND
            k.reisedato >= ?
    """
    res = cur.execute(upcoming_trips_sql, (customer_ID, current_date))
    upcoming_trips_data = res.fetchall()

    print("Hello", customer_name + "!")
    if len(upcoming_trips_data) == 0:
        print("You have no upcoming trips!")
    else:
        print("Here are your upcoming trips:")
        for row in upcoming_trips_data:
            print()
            print("Ordrenummer " + str(row[0]) + ". Kjøpt " + row[1])
            print("Linje " + str(row[2]))
            print("Dato: " + row[3])
            print(row[7] + " - " + row[8])
            print("Billettnummer " + str(row[4]))
            print("Vogn ID: " + str(row[5]))
            print("Plass nummer " + str(row[6]))
    print()