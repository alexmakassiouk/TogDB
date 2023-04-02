import sqlite3

con = sqlite3.connect("../tog.db")
cur = con.cursor()

# jernbanestasjon(navn, moh)
station_data = [ 
    ("Trondheim S", 5.1),
    ("Steinkjer", 3.6),
    ("Mosjøen", 6.8),
    ("Mo i Rana", 3.5),
    ("Fauske", 34),
    ("Bodø", 4.1)
]

# banestrekning(ID, navn, dobbeltspor, startstasjon, endestasjon)
nordlandsbanen_data = ("Nordlandsbanen", 1, "Trondheim S", "Bodø")

# delstrekning(ID, lengde, dobbeltspor, stasjon1, stasjon2)
section_data = [
    (1, 120, 1, "Trondheim S", "Steinkjer"),
    (2, 280, 0, "Steinkjer", "Mosjøen"),
    (3, 90, 0, "Mosjøen", "Mo i Rana"),
    (4, 170, 0, "Mo i Rana", "Fauske"),
    (5, 60, 0, "Fauske", "Bodø")
]

# banestrekning_delstrekninger(banestrekningID, delstrekningID)
nordlandsbanen_section_data = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5)
]

# banestrekning_stoppestasjoner(banestrekningID, jernbanestasjonNavn)
nordlandsbanen_station_data = [
    (1, "Trondheim S"),
    (1, "Steinkjer"),
    (1, "Mosjøen"),
    (1, "Mo i Rana"),
    (1, "Fauske"),
    (1, "Bodø")
]


def insert_railway_data(stations, railways, sections, railway_sections, railway_stations):
    cur.executemany("INSERT INTO jernbanestasjon VALUES(?, ?)", stations)
    con.commit()

    cur.executemany("INSERT INTO banestrekning(navn, elektrisk, startstasjon, endestasjon) VALUES(?, ?, ?, ?)", railways)
    con.commit()

    cur.executemany("INSERT INTO delstrekning VALUES(?, ?, ?, ?, ?)", sections)
    con.commit()

    cur.executemany("INSERT INTO banestrekning_delstrekninger VALUES(?, ?)", railway_sections)
    con.commit()

    cur.executemany("INSERT INTO banestrekning_stoppestasjoner VALUES(?, ?)", railway_stations)
    con.commit()



def print_inserted_data():
    print("Inserted data for Nordlandsbanen:")
    print("Stations:")
    for row in cur.execute("SELECT * FROM jernbanestasjon"):
        print(row)
    print()
    print("Banestrekning:")
    res = cur.execute("SELECT * FROM banestrekning")
    print(res.fetchall())
    print()
    print("Delstrekninger in corresponding Banestrekning:")
    for row in cur.execute("""
                        SELECT 
                          d.ID, d.lengde, d.dobbeltspor, d.stasjon1, d.stasjon2, b.navn AS tilhørerBanestrekning, b.elektrisk 
                        FROM 
                          delstrekning AS d
                        INNER JOIN 
                          banestrekning_delstrekninger AS bd 
                        ON 
                          (d.ID = bd.delstrekningID)
                        INNER JOIN 
                          banestrekning AS b 
                        ON 
                          (b.ID = bd.banestrekningID)
                        """):
        print(row)
    print()
    print("All stations on each banestrekning:")
    for row in cur.execute("""
                            SELECT 
                              b.navn, j.navn
                            FROM 
                              banestrekning AS b 
                            INNER JOIN 
                              banestrekning_stoppestasjoner AS bs 
                            ON 
                              (b.ID = bs.banestrekningID)
                            INNER JOIN 
                              jernbanestasjon AS j 
                            ON 
                              (bs.jernbanestasjonNavn = j.navn)
                            """):
        print(row)


# UNCOMMENT TO INSERT DATA AND PRINT

#insert_railway_data(stations=station_data, railways=nordlandsbanen_data, sections=section_data, 
#                    railway_sections=nordlandsbanen_section_data, railway_stations=nordlandsbanen_station_data)
# print_inserted_data()