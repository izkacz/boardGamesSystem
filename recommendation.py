import pandas as pd

from flask import request
import csv


def makeRecommendation():
    return

def genre_choosing(genre):
    df = pd.read_csv('categories_data.csv')
    df2 = pd.read_csv('basic_data.csv')
    gamesVotes = []
    gamesTitles = []
    for index, row in df.iterrows():
        if row[genre] == 1:
            gamesVotes.append(row['bayes_rating'])
            if len(gamesVotes) == 1:
                break
    for vote in gamesVotes:
        for index, row in df2.iterrows():
            if row['bayes_rating'] == vote:
                gamesTitles.append(row['name'])
    print(gamesTitles)
    return gamesTitles[0:]
