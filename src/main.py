from departures import departures_main
from user import user_main
from search import search_main
from find_tickets import find_tickets_main
from upcoming_trips import upcoming_trips_main

def option_one():
    print("You selected option 1")
    # User story c)
    departures_main()

def option_two():
    print("You selected option 2")
    # User story e)
    user_main()

def option_three():
    print("You selected option 3")
    # User story d)
    search_main()

def option_four():
    print("You selected option 4")
    # User story g)
    find_tickets_main()
def option_five():
    print("You selected option 5")
    # User story h)
    upcoming_trips_main()

# Simple main menu from where all other user stories can be explored
def show_menu():
    choice = " "
    while choice != "exit":
        print("Menu:")
        print("1. Trainroutes at a station")
        print("2. Register user")
        print("3. Search travel")
        print("4. Find available tickets")
        print("5. See upcoming trips")
        print("9. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            option_one()
        elif choice == "2":
            option_two()
        elif choice == "3":
            option_three()
        elif choice == "4":
            option_four()
        elif choice == "5":
            option_five()
        elif choice == "exit" or choice == "9":
            break
        else:
            print("Invalid choice")

show_menu()