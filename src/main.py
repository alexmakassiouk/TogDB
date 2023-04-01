from departures import departures_main
from user import user_main
from search import search_main
from find_tickets import find_tickets_main

def option_one():
    print("You selected option 1")
    departures_main()

def option_two():
    print("You selected option 2")
    user_main()

def option_three():
    print("You selected option 3")
    search_main()

def option_four():
    print("You selected option 4")
    find_tickets_main()

def show_menu():
    choice = " "
    while choice != "exit":
        print("Menu:")
        print("1. Trainroutes at a station")
        print("2. Register user")
        print("3. Search travel")
        print("4. Find available tickets")
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
        elif choice == "exit" or choice == "9":
            break
        else:
            print("Invalid choice")

show_menu()