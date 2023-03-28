from departures import departures_main
from user import user_main

def option_one():
    print("You selected option 1")
    departures_main()

def option_two():
    print("You selected option 2")
    user_main()

def option_three():
    print("You selected option 3")

def show_menu():
    choice = " "
    while choice != "exit":
        print("Menu:")
        print("1. Trainroutes at a station")
        print("2. Register user")
        print("3. Option 3")
        choice = input("Enter your choice: ")
        if choice == "1":
            option_one()
        elif choice == "2":
            option_two()
        elif choice == "3":
            option_three()
        elif choice == "exit":
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    show_menu()