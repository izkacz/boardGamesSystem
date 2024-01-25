import pandas as pd

from flask import request
import csv


def makeRecommendation():
    return

def genre_choosing(genre):
    df = pd.read_csv('spotify_songs_cleaned.csv')
    songsWithGenre = []
    for index, row in df.iterrows():
        if row['playlist_genre'] == genre.lower():
            songsWithGenre.append(row['track_name'])
    print(songsWithGenre)
    return songsWithGenre
