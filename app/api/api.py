import time
from flask import Flask
import sqlite3
import json
import random
import sys
sys.path.append("../../comment_finder")
import inference
from flask import request

app = Flask(__name__)

streams = []
choice = {}
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
            "serie": (False if title[1] == 0 else True),
            "year": title[2],
            "directors": title[3].split(", "),
            "actors": title[4].split(", "),
            "genres": title[5].split(", "),
            "posters": title[6].split(", "),
        })


def get_recommendation():
    max_val = 0
    best_movie = random.choice(streams)
    for title in streams:
        current_val = 0
        for genre in title['genres']:
            try:
                current_val += freq_map['genres'][genre]
            except KeyError:
                pass
        if current_val > max_val:
            best_movie = title
    streams.remove(best_movie)
    print(freq_map['genres'])
    return best_movie

@app.route('/semantic', methods = ['POST'])
def semantic():
    print(request.json)
    sentence = request.json['sentence']
    return inference.api_answer(sentence)

@app.route('/like')
def like():
    global choice
    """
    User liked the recommendation, update weights accordingly, find max weighted movie in the same loop, return it as the recommendation
    """
    for director in choice['directors']:
        try:
            freq_map['directors'][director] += 1
        except KeyError:
            freq_map['directors'][director] = 1
    for actor in choice['actors']:
        try:
            freq_map['actors'][actor] += 1
        except KeyError:
            freq_map['actors'][actor] = 1
    try:
        freq_map['years'][choice['year']] += 1
    except KeyError:
        freq_map['years'][choice['year']] = 1
    for genres in choice['genres']:
        try:
            freq_map['genres'][genres] += 1
        except KeyError:
            freq_map['genres'][genres] = 1

    movie = get_recommendation()
    choice = movie
    return movie

@app.route('/dislike')
def dislike():
    global choice
    """
    User did not like the recommendation, update weights accordingly, find max weighted movie in the same loop, return it as the recommendation
    """
    for director in choice['directors']:
        try:
            freq_map['directors'][director] -= 1
        except KeyError:
            freq_map['directors'][director] = -1
    for actor in choice['actors']:
        try:
            freq_map['actors'][actor] -= 1
        except KeyError:
            freq_map['actors'][actor] = -1
    try:
        freq_map['years'][choice['year']] -= 1
    except KeyError:
        freq_map['years'][choice['year']] = -1
    for genres in choice['genres']:
        try:
            freq_map['genres'][genres] -= 1
        except KeyError:
            freq_map['genres'][genres] = -1
    movie = get_recommendation()
    choice = movie
    return movie

@app.route('/init')
def init():
    return random_choice()

def random_choice():
    global choice
    choice = random.choice(streams)
    streams.remove(choice)
    return choice
    
load_streams()