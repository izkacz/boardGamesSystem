import time
from urllib.parse import urljoin
from urllib.request import urlopen

import pandas as pd
import requests
from bs4 import BeautifulSoup

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

    # url = "https://boardgamegeek.com/browse/boardgamecategory"
    # page = urlopen(url)
    # html = page.read().decode("utf-8")
    # soup = BeautifulSoup(html, "html.parser")
    # links = [urljoin(url, a.get('href')) for a in soup.find_all('a', href=True)]
    # links = set(links)
    # for link in links:
    #     if genre in link:
    #         print(link)
    #         page2 = urlopen(link)
    #         html2 = page2.read().decode("utf-8")
    #         newSoup = BeautifulSoup(html2, "html.parser")
    #         # topGames = newSoup.find('a',href=True)
    #         print(newSoup)
