def option_one():
    print("You selected option 1")

def option_two():
    print("You selected option 2")

def option_three():
    print("You selected option 3")

def show_menu():
    print("Menu:")
    print("1. Option 1")
    print("2. Option 2")
    print("3. Option 3")

    choice = input("Enter your choice: ")
    if choice == "1":
        option_one()
    elif choice == "2":
        option_two()
    elif choice == "3":
        option_three()
    else:
        print("Invalid choice")

if __name__ == '__main__':
    show_menu()