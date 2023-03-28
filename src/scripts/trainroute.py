import sqlite3

con = sqlite3.connect("./tog.db")
cur = con.cursor()

operator_data = [(1, "SJ")]

cur.executemany("INSERT INTO operator VALUES(?, ?)", operator_data)
con.commit()

carriagetype_data = [
    ("SJ-sittevogn-1", 1, None, 3, 4),
    ("SJ-sovevogn-1", 1, 4, None, None)
]

cur.executemany("INSERT INTO vogntype VALUES(?, ?, ?, ?, ?)", carriagetype_data)
con.commit()