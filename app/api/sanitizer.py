import sqlite3
import json

con = sqlite3.connect("data/BurdaData.db")
cur = con.cursor()
values = [
    'id',
    'available',
    'imdb_id',
    'title',
    'otitle',
    'original',
    'serie',
    'season',
    'year',
    'directors',
    'actors',
    'companies',
    'countries',
    'genres',
    'channel',
    'banners',
    'posters',
    'pid',
    'provider',
    'url',
    'seasonurl',
    'episodeurl',
    'type',
    'language'
    ]
cur.execute("""CREATE TABLE IF NOT EXISTS data(
    id int NOT NULL,
    available,
    imdb_id, 
    title, 
    otitle, 
    original, 
    serie, 
    season, 
    year, 
    directors, 
    actors, 
    companies, 
    countries, 
    genres, 
    channel, 
    banners, 
    posters, 
    pid, 
    provider, 
    url, 
    seasonurl, 
    episodeurl, 
    type, 
    language,
    PRIMARY KEY (id))""")

with open('data/nf.json') as f:
    d = json.load(f)
    for entry in d:
        print(entry)
        s = "INSERT INTO data VALUES("
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
            cur.execute(f"{s}\"{entry[values[-1]]}\")")
            con.commit()
        except sqlite3.IntegrityError:
            pass