-- tables

-- Table: jernbanestasjon
CREATE TABLE jernbanestasjon (
    navn TEXT PRIMARY KEY,
    moh REAL
);

-- Table: delstrekning
CREATE TABLE delstrekning (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    lengde REAL,
    dobbeltspor INTEGER,
    stasjon1 TEXT NOT NULL,
    stasjon2 TEXT NOT NULL,
    FOREIGN KEY (stasjon1)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (stasjon2)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

-- Table: banestrekning
CREATE TABLE banestrekning (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    navn TEXT,
    elektrisk INTEGER,
    startstasjon TEXT NOT NULL,
    endestasjon TEXT NOT NULL,
    FOREIGN KEY (startstasjon)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (endestasjon)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: banestrekning_delstrekninger
CREATE TABLE banestrekning_delstrekninger (
    banestrekningID INTEGER NOT NULL,
    delstrekningID INTEGER NOT NULL,
    PRIMARY KEY (banestrekningID, delstrekningID),
    FOREIGN KEY (banestrekningID)
        REFERENCES banestrekning (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (delstrekningID)
        REFERENCES delstrekning (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: banestrekning_stoppestasjoner
CREATE TABLE banestrekning_stoppestasjoner (
    banestrekningID INTEGER NOT NULL,
    jernbanestasjonNavn TEXT NOT NULL,
    PRIMARY KEY (banestrekningID, jernbanestasjonNavn),
    FOREIGN KEY (banestrekningID)
        REFERENCES banestrekning (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (jernbanestasjonNavn)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: ukedag
CREATE TABLE ukedag (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    navn TEXT UNIQUE
);

--Table: operator
CREATE TABLE operator (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    navn TEXT
);

--Table: togrute
CREATE TABLE togrute (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    startstasjon TEXT NOT NULL,
    avgangstid TEXT,
    endestasjon TEXT NOT NULL,
    ankomsttid TEXT,
    operatorID INTEGER NOT NULL,
    FOREIGN KEY (startstasjon)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (endestasjon)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (operatorID)
        REFERENCES operator (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: togrute_stoppestasjon
CREATE TABLE togrute_stoppestasjon (
    togruteID INTEGER NOT NULL,
    jernbanestasjonNavn TEXT NOT NULL,
    ankomsttid TEXT,
    avgangstid TEXT,
    PRIMARY KEY (togruteID, jernbanestasjonNavn),
    FOREIGN KEY (togruteID)
        REFERENCES togrute (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (jernbanestasjonNavn)
        REFERENCES jernbanestasjon (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: togrute_ukedager
CREATE TABLE togrute_ukedager (
    togruteID INTEGER NOT NULL,
    ukedagID INTEGER NOT NULL,
    PRIMARY KEY (togruteID, ukedagID),
    FOREIGN KEY (togruteID)
        REFERENCES togrute (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (ukedagID)
        REFERENCES ukedag (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: togruteforekomst
CREATE TABLE togruteforekomst (
    togruteID INTEGER NOT NULL,
    dato TEXT,
    PRIMARY KEY (togruteID, dato),
    FOREIGN KEY (togruteID)
        REFERENCES togrute (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: vogntype
CREATE TABLE vogntype (
    navn TEXT PRIMARY KEY,
    operatorID INTEGER,
    antall_sovekupeer INTEGER,
    antall_rader INTEGER,
    seter_per_rad INTEGER,
    FOREIGN KEY (operatorID)
        REFERENCES operator (ID)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

--Table: vogn
CREATE TABLE vogn (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    vogntypeNavn TEXT NOT NULL,
    FOREIGN KEY (vogntypeNavn)
        REFERENCES vogntype (navn)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: togrute_vogn_oppsett
CREATE TABLE togrute_vogn_oppsett (
    togruteID INTEGER NOT NULL,
    vognID INTEGER NOT NULL,
    nummer_fra_front INTEGER,
    PRIMARY KEY (togruteID, vognID),
    FOREIGN KEY (togruteID)
        REFERENCES togrute (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (vognID)
        REFERENCES vogn (ID)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

--Table: kunde
CREATE TABLE kunde (
    kundenummer INTEGER PRIMARY KEY AUTOINCREMENT,
    navn TEXT,
    epost TEXT UNIQUE,
    mobilnummer INTEGER UNIQUE
);

--Table: kundeordre
CREATE TABLE kundeordre (
    ordrenummer INTEGER PRIMARY KEY AUTOINCREMENT,
    kjopstidspunkt TEXT,
    kundenummer INTEGER,
    togruteID INTEGER,
    reisedato TEXT,
    FOREIGN KEY (kundenummer)
        REFERENCES kunde (kundenummer)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (togruteID)
        REFERENCES togruteforekomst (togruteID)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (reisedato)
        REFERENCES togruteforekomst (dato)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

--Table: billett
CREATE TABLE billett (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    plassnummer INTEGER,
    pastigning TEXT,
    avstigning TEXT,
    ordrenummer INTEGER NOT NULL,
    vognID INTEGER,
    FOREIGN KEY (pastigning)
        REFERENCES jernbanestasjon (navn)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (avstigning)
        REFERENCES jernbanestasjon (navn)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
    FOREIGN KEY (ordrenummer)
        REFERENCES kundeordre (ordrenummer)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (vognID)
        REFERENCES vogn (ID)
            ON DELETE SET NULL
            ON UPDATE CASCADE
);

-- insert values

-- These are probably to be inserted with the python script

-- INSERT INTO jernbanestasjon (navn, moh)
-- VALUES
--     ("Trondheim S", 5.1),
--     ("Steinkjer", 3.6),
--     ("Mosjøen", 6.8),
--     ("Mo i Rana", 3.5),
--     ("Fauske", 34),
--     ("Bodø", 4.1);

-- INSERT INTO operator (ID, navn)
-- VALUES(1, "SJ");

-- INSERT INTO vogntype (navn, operatorID, antall_sovekupeer, antall_rader, seter_per_rad)
-- VALUES
--     ("SJ-sittevogn-1", 1, NULL, 3, 4),
--     ("SJ-sovevogn-1", 1, 4, NULL, NULL);

-- INSERT INTO togrute (ID, startstasjon, avgangstid, endestasjon, ankomsttid, operatorID)
-- VALUES
--     (1, "Trondheim S", "07:49", "Bodø", "17:34", 1),
--     (2, "Trondheim S", "23:05", "Bodø", "09:05", 1),
--     (3, "Mo i Rana", "08:11", "Trondheim S", "14:13", 1);

-- INSERT INTO ukedag (ID, navn)
-- VALUES
--     (1, "mandag"),
--     (2, "tirsdag"),
--     (3, "onsdag"),
--     (4, "torsdag"),
--     (5, "fredag"),
--     (6, "lørdag"),
--     (7, "søndag");

-- INSERT INTO togrute_ukedager (togruteID, ukedagID)
-- VALUES
--     (1, 1),
--     (1, 2),
--     (1, 3),
--     (1, 4),
--     (1, 5),
--     (2, 1),
--     (2, 2),
--     (2, 3),
--     (2, 4),
--     (2, 5),
--     (2, 6),
--     (2, 7),
--     (3, 1),
--     (3, 2),
--     (3, 3),
--     (3, 4),
--     (3, 5);

-- INSERT INTO vogn (ID, vogntypeNavn)
-- VALUES
--     (1, "SJ-sittevogn-1"),
--     (2, "SJ-sittevogn-1"),
--     (3, "SJ-sittevogn-1"),
--     (4, "SJ-sovevogn-1"),
--     (5, "SJ-sittevogn-1");

-- INSERT INTO togrute_vogn_oppsett (togruteID, vognID, nummer_fra_front)
-- VALUES
--     (1, 1, 1),
--     (1, 2, 2),
--     (2, 3, 1),
--     (2, 4, 2),
--     (3, 5, 1);

-- INSERT INTO togrute_stoppestasjon (togruteID, jernbanestasjonNavn, ankomsttid, avgangstid)
-- VALUES
--     (1, "Steinkjer", "09:51", "09:51"),
--     (1, "Mosjøen", "13:20", "13:20"),
--     (1, "Mo i Rana", "14:31", "14:31"),
--     (1, "Fauske", "16:49", "16:49"),
--     (2, "Steinkjer", "00:57", "00:57"),
--     (2, "Mosjøen", "04:41", "04:41"),
--     (2, "Mo i Rana", "05:55", "05:55"),
--     (2, "Fauske", "08:19", "08:19"),
--     (3, "Mosjøen", "09:14", "09:14"),
--     (3, "Steinkjer", "12:31", "12:31");