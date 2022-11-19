import time
from flask import Flask
import sqlite3
import json
import random
import numpy as np

app = Flask(__name__)

streams = []
choices = []
freq_map = {
    'years': {},
    'directors': {},
    'actors': {},
    'genres': {},
}
norm_val=[0.32,0.6,0.88,1,0.88,0.6,0.32]

year_weighted=dict.fromkeys(range(1915,2023),0)

total_actors={}

total_directors={}

total_genres={}

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
    #year
    current_year=list(freq_map['years'].keys())[0]
    point_year=list(freq_map['years'].values())[0]
    for i in range(-3,4):
        year_weighted[current_year+i]=point_year*norm_val[i+3]
    #actor
    actors=list(freq_map['actors'].keys())
    point_actor=list(freq_map['years'].values())[0]
    exp_vala=list(range(0,len(list(freq_map['actors'].keys()))))
    exp_vala=np.multiply(-0.3,exp_vala)
    exp_vala=np.exp(exp_vala)
    for i in range(0,len(actors)):
        if actors[i] in total_actors:
            total_actors[actors[i]]+=exp_vala[i]*point_actor
        if actors[i] not in total_actors:
            total_actors[actors[i]]=exp_vala[i]*point_actor
    #director
    directors=list(freq_map['directors'].keys())
    point_director=list(freq_map['directors'].values())[0]
    exp_vald=list(range(0,len(list(freq_map['directors'].keys()))))
    exp_vald=np.multiply(-0.1,exp_vald)
    exp_vald=np.exp(exp_vald)
    for i in range(0,len(directors)):
        if directors[i] in total_directors:
            total_directors[directors[i]]+=exp_vald[i]*point_director
        if directors[i] not in total_directors:
            total_directors[directors[i]]=exp_vald[i]*point_director
    #genres
    genres=list(freq_map['genres'].keys())
    point_genres=list(freq_map['genres'].values())[0]
    for i in range(0,len(genres)):
        if genres[i] in total_genres:
            total_genres[genres[i]]+=point_genres
        if genres[i] not in total_genres:
            total_genres[genres[i]]=point_genres          
def get_movie():
#finding the best movie
    best_sum=0
    for current_movie in range(0,len(streams)):
        year_movie=list(streams[current_movie].values())[2]
        print(year_movie)
        print(list(streams[current_movie].values())[0])
        current_sum=year_weighted[int(year_movie)]
            
        dir=list(streams[current_movie].values())[3]
        for current_dir in range(len(dir)):
            if dir[current_dir] in total_directors.values():
                current_sum+=total_directors[dir[current_dir]]
                    
        act=list(streams[current_movie].values())[4]
        for current_act in range(len(act)):
            if act[current_act] in total_actors.values():
                current_sum+=total_actors[dir[current_act]]
                    
        gen=list(streams[current_movie].values())[5]
        for current_gen in range(len(gen)):
            if gen[current_gen] in total_genres.values():
                current_sum+=total_genres[dir[current_gen]]
            #if current_sum>best_sum:
                #best_sum=current_sum    

    
    
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
def dislike():
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
#choice = random.choice(streams)
choice=streams[3]
streams.remove(choice)
choices.append(choice)
dislike()
dislike()
#get_recommendation()
get_movie()
#print(year_weighted[2015])
#print(year_weighted)
#print(year_weighted[list(streams[10].values())[2]])
#print(list(streams[5].values())[0])
#print(list(streams[5].values())[2])
#print(list(streams[2766].values())[2])
#print(list(year_weighted)[0])
#print(list(list(streams[3].values())[3])[0])