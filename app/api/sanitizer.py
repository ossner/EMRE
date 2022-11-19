import sqlite3
import json

con = sqlite3.connect("data/BurdaData.db")
cur = con.cursor()
values = [
    'id',
    'title',
    'otitle',
    'serie', 
    'year', 
    'directors', 
    'actors', 
    'genres', 
    'posters', 
    ]
cur.execute("""CREATE TABLE IF NOT EXISTS streams(
    id int NOT NULL,
    title UNIQUE, 
    otitle NOT NULL,
    serie NOT NULL, 
    year NOT NULL, 
    directors NOT NULL, 
    actors NOT NULL, 
    genres NOT NULL, 
    posters NOT NULL, 
    PRIMARY KEY (id))""")

with open('data/dp.json') as f:
    d = json.load(f)
    for entry in d:
        print(entry)
        s = "INSERT INTO streams VALUES("
        for value in values[:-1]:
            v = entry[value]
            if v:
                v = v.replace('\"', '')
                try:
                    int(v)
                    s += f"{v}, "
                except ValueError:
                    s += f"\"{v}\", "

            else:
                s += "null, "
        print(f"{s}\"{entry[values[-1]]}\")")
        try:
            v = entry[values[-1]]
            if v:
                v = v.replace('\"', '')
                try:
                    int(v)
                    s += f"{v}"
                except ValueError:
                    s += f"\"{v}\""

            else:
                s += "null"
            cur.execute(f"{s})")
            con.commit()
        except sqlite3.IntegrityError:
            pass