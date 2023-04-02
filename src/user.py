import sqlite3
import re

con = sqlite3.connect("tog.db")
cur = con.cursor()

# Create user
def user_main():
    name = input("What is your name? ")
    email = input("What is your e-mail? ")
    while not is_valid_email(email):
        email = input("Invalid email. Please try again: ")
    phone = input("And lastly, what is your phone number? ")
    while not is_valid_phone(phone):
        phone = input("Invalid phone. Please try again: ") 
    post_user(name, email, phone)

def is_valid_email(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
        return True
    return False
    
def is_valid_phone(phone: str):
    if phone.isdigit():
        return True
    return False
def post_user(name, email, phone):
    sql = f"""
    INSERT INTO kunde(navn, epost, mobilnummer) VALUES(?, ?, ?)
    """
    # Cannot have already existing phone and email. Those values are UNIQUE
    try:
        cur.execute(sql, (name, email, phone))
        con.commit()
        print("Thank you,", name + ".", "Your account is now created")
    except sqlite3.IntegrityError:
        print("That phone number or e-mail already exists! Please choose another one!")
        answer = input("Would you like to try again? (y/n) ")
        if answer == "y":
            user_main()
        else:
            pass