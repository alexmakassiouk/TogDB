import sqlite3

con = sqlite3.connect("../tog.db")
cur = con.cursor()

### TABLE DATA ###

# operator(ID, navn)
operator_data = [(1, "SJ")]

# vogntype(navn, operatorID, antall_sovekupeer, antall_rader, seter_per_rad)
carriagetype_data = [
    ("SJ-sittevogn-1", 1, None, 3, 4),
    ("SJ-sovevogn-1", 1, 4, None, None)
]

# togrute(ID, startstasjon, avgangstid, endestasjon, ankomsttid, operatorID)
trainroute_data = [
    (1, "Trondheim S", "07:49", "Bodø", "17:34", 1),
    (2, "Trondheim S", "23:05", "Bodø", "09:05", 1),
    (3, "Mo i Rana", "08:11", "Trondheim S", "14:13", 1)
]

# ukedag(ID, navn)
weekday_data = [
    (1, "mandag"),
    (2, "tirsdag"),
    (3, "onsdag"),
    (4, "torsdag"),
    (5, "fredag"),
    (6, "lørdag"),
    (7, "søndag")
]

# togrute_ukedager(togruteID, ukedagID)
trainroute_weekday_data = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5)
]

# vogn(ID, vogntypeNavn)
carriage_data = [
    (1, "SJ-sittevogn-1"),
    (2, "SJ-sittevogn-1"),
    (3, "SJ-sittevogn-1"),
    (4, "SJ-sovevogn-1"),
    (5, "SJ-sittevogn-1")
]

# togrute_vogn_oppsett(togruteID, vognID, nummer_fra_front)
trainroute_carriage_setup_data = [
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (2, 4, 2),
    (3, 5, 1)
]

# togrute_stoppestasjon(togruteID, jernbanestasjonNavn, ankomsttid, avgangstid)
trainroute_stop_data = [
    (1, "Steinkjer", "09:51", "09:51"),
    (1, "Mosjøen", "13:20", "13:20"),
    (1, "Mo i Rana", "14:31", "14:31"),
    (1, "Fauske", "16:49", "16:49"),
    (2, "Steinkjer", "00:57", "00:57"),
    (2, "Mosjøen", "04:41", "04:41"),
    (2, "Mo i Rana", "05:55", "05:55"),
    (2, "Fauske", "08:19", "08:19"),
    (3, "Mosjøen", "09:14", "09:14"),
    (3, "Steinkjer", "12:31", "12:31")
]

def insert_trainroute_data(operators, carriagetypes, trainroutes, weekdays, trainroute_weekdays, carriages, trainroute_carriage_setup, trainroute_stops):

    cur.executemany("INSERT INTO operator VALUES(?, ?)", operators)
    con.commit()
    
    cur.executemany("INSERT INTO vogntype VALUES(?, ?, ?, ?, ?)", carriagetypes)
    con.commit()
    
    cur.executemany("INSERT INTO togrute VALUES(?, ?, ?, ?, ?, ?)", trainroutes)
    con.commit()
    
    cur.executemany("INSERT INTO ukedag VALUES(?, ?)", weekdays)
    con.commit()

    cur.executemany("INSERT INTO togrute_ukedager VALUES(?, ?)", trainroute_weekdays)
    con.commit()
    
    cur.executemany("INSERT INTO vogn VALUES(?, ?)", carriages)
    con.commit()

    cur.executemany("INSERT INTO togrute_vogn_oppsett VALUES(?, ?, ?)", trainroute_carriage_setup)
    con.commit()

    cur.executemany("INSERT INTO togrute_stoppestasjon VALUES(?, ?, ?, ?)", trainroute_stops)
    con.commit()

def print_trainroute_data():
    print("Inserted data for trainroutes on Nordlandsbanen:")
    print("Operators:")
    for row in cur.execute("SELECT * FROM operator"):
        print(row)
    print()
    print("Carriage types:")
    for row in cur.execute("SELECT * FROM vogntype"):
        print(row)
    print()
    print("Trainroutes")
    for row in cur.execute("SELECT * FROM togrute"):
        print(row)
    print()
    print("Trainroute weekdays:")
    for row in cur.execute("""
                            SELECT 
                              t.ID, t.startstasjon, t.avgangstid, t.endestasjon, o.navn, u.navn
                            FROM 
                              togrute AS t
                            INNER JOIN 
                              togrute_ukedager AS tu 
                            ON 
                              (t.ID = tu.togruteID)
                            INNER JOIN 
                              ukedag AS u 
                            ON 
                              (tu.ukedagID = u.ID)
                            INNER JOIN 
                              operator AS o 
                            ON 
                              (t.operatorID = o.ID)
                            """):
        print(row)

    print()
    print("Available carriages:")
    for row in cur.execute("SELECT * FROM vogn"):
        print(row)
    print()
    print("Carriages on trainroutes:")
    for row in cur.execute("""
                            SELECT 
                              tvo.togruteID, tvo.nummer_fra_front, v.ID, vt.navn
                            FROM 
                              togrute_vogn_oppsett AS tvo
                            INNER JOIN 
                              vogn AS v 
                            ON 
                              (tvo.vognID = v.ID)
                            INNER JOIN 
                              vogntype AS vt 
                            ON 
                              (v.vogntypeNavn = vt.navn)
                            ORDER BY 
                              tvo.togruteID, tvo.nummer_fra_front
                            """):
        print(row)
    print()
    print("Trainroute tables:")
    trainRouteID = 0
    for row in cur.execute("SELECT * FROM togrute_stoppestasjon"):
        if(trainRouteID != row[0]):
            cur2 = con.cursor()
            #Endestasjon på den forrige togruten
            res = cur2.execute(f'SELECT t.ID, t.endestasjon, t.ankomsttid FROM togrute AS t WHERE t.ID = {trainRouteID}').fetchone()
            if res != None:
                print(res)
            #Linjeskift før neste togrute
            print()
            #Startstasjon på ny togrute
            print(cur2.execute(f'SELECT t.ID, t.startstasjon, t.avgangstid FROM togrute AS t WHERE t.ID = {trainRouteID+1}').fetchone())
        print(row)
        trainRouteID = row[0]
    print(cur2.execute(f'SELECT t.ID, t.endestasjon, t.ankomsttid FROM togrute AS t WHERE t.ID = {trainRouteID}').fetchone())

## Uncomment next lines to add initial data to DB
#insert_trainroute_data(operators=operator_data, carriagetypes=carriagetype_data, trainroutes=trainroute_data, weekdays=weekday_data, trainroute_weekdays=trainroute_weekday_data, carriages=carriage_data, trainroute_carriage_setup=trainroute_carriage_setup_data, trainroute_stops=trainroute_stop_data)
# print_trainroute_data()
con.close()