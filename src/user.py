import sqlite3

con = sqlite3.connect("tog.db")
cur = con.cursor()

def user_main():
    name = input("What is your name? ")
    email = input("What is your e-mail? ")
    phone = input("And lastly, what is your phone number? ")
    post_user(name, email, phone)

    

def post_user(name, email, phone):
    sql = f"""
    INSERT INTO kunde(navn, epost, mobilnummer) VALUES('{name}', '{email}', '{phone}')
    """
    try:
        cur.execute(sql)
        con.commit()
        print("Thank you,", name + ".", "Your account is now created")
    except sqlite3.IntegrityError:
        print("That phone number or e-mail already exists! Please choose another one!")
        answer = input("Would you like to try again? (y/n) ")
        if answer == "y":
            user_main()
        else:
            pass