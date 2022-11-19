import time
from flask import Flask
import sqlite3
import json
import random

app = Flask(__name__)

streams = []
choices = []
freq_map = {
    'years': {},
    'directors': {},
    'actors': {},
    'genres': {},
}

def load_streams():
    """
    On startup, load information relevant for weighting into streams list from database
    """
    con = sqlite3.connect("../../data/BurdaData.db")
    cur = con.cursor()
    ids = cur.execute("SELECT id FROM streams")
    ids = ids.fetchall()
    for num in ids:
        title = cur.execute(f"SELECT title, serie, year, directors, actors, genres, posters FROM streams WHERE id={num[0]}")
        title = title.fetchone()
        streams.append({
            "title": title[0],
            "serie": (True if title[1] == 0 else False),
            "year": title[2],
            "directors": title[3].split(", "),
            "actors": title[4].split(", "),
            "genres": title[5].split(", "),
            "posters": title[6].split(", "),
        })


def get_recommendation():
    pass


@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/like')
def like():
    """
    User liked the recommendation, update weights accordingly, find max weighted movie in the same loop, return it as the recommendation
    """
    print(freq_map)
    for director in choices[-1]['directors']:
        try:
            freq_map['directors'][director] += 1
        except KeyError:
            freq_map['directors'][director] = 1
    for actor in choices[-1]['actors']:
        try:
            freq_map['actors'][actor] += 1
        except KeyError:
            freq_map['actors'][actor] = 1
    try:
        freq_map['years'][choices[-1]['year']] += 1
    except KeyError:
        freq_map['years'][choices[-1]['year']] = 1
    for genres in choices[-1]['genres']:
        try:
            freq_map['genres'][genres] += 1
        except KeyError:
            freq_map['genres'][genres] = 1

    return freq_map

@app.route('/dislike')
def dislke():
    """
    User did not like the recommendation, update weights accordingly, find max weighted movie in the same loop, return it as the recommendation
    """
    for director in choices[-1]['directors']:
        try:
            freq_map['directors'][director] -= 1
        except KeyError:
            freq_map['directors'][director] = -1
    for actor in choices[-1]['actors']:
        try:
            freq_map['actors'][actor] -= 1
        except KeyError:
            freq_map['actors'][actor] = -1
    try:
        freq_map['years'][choices[-1]['year']] -= 1
    except KeyError:
        freq_map['years'][choices[-1]['year']] = -1
    for genres in choices[-1]['genres']:
        try:
            freq_map['genres'][genres] -= 1
        except KeyError:
            freq_map['genres'][genres] = -1
    return None

load_streams()
choice = random.choice(streams)
streams.remove(choice)
choices.append(choice)