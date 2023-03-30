import sqlite3
from search import construct_query

con = sqlite3.connect("src/tog.db")
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
find_tickets_main()