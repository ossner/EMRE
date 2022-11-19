import torch
import faiss
from sentence_transformers import SentenceTransformer
import scipy.spatial.distance as distance
import pandas as pd
import numpy as np

indexer = faiss.read_index('hnsw.index')
model = SentenceTransformer("sentence-transformers/distiluse-base-multilingual-cased-v2")
df = pd.read_csv('all_end.csv')
embeds = np.load('all_end.npy')


def search_movie(text, indexer, df, sug_count=5):
    with torch.no_grad():
        s1 = model.encode(text)
    print(s1.shape)
    out = indexer.search(s1[np.newaxis,:], 100)
    out_index = out[1][0]
    
    cos_list = []
    for idx in out_index:
        movie_embed = embeds[idx]
        cos_distance = distance.cosine(s1, movie_embed)
        l2_distance = np.linalg.norm(s1 - movie_embed)
        cos_list.append([idx, l2_distance])
        
    cos_list = sorted(cos_list, key=lambda x: x[1])[:sug_count]
    idx_ordered = [i for i, _ in cos_list]
    cos_ordered = [j for _, j in cos_list]
    
    return df.iloc[idx_ordered], cos_ordered


def api_answer(sentence):
    out_df, cos = search_movie(sentence, indexer, df)
    item_array = []
    for idx, cos_dist in enumerate(cos):
        item = out_df.iloc[idx]
        print(f"{item.Title} - {item.Year}")
        print(f"{item.Poster}")
        print(f"{item.Plot}")
        print(cos_dist)
        item_dict = {
            "plot" : item.Plot,
            "poster": item.Poster,
            "title": item.Title,
            "year" : item.Year
        }
        item_array.append(item_dict)
    return item_array