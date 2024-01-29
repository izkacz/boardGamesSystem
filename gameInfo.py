from urllib.parse import urljoin
from urllib.request import urlopen
import os

import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
import itertools
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
dataset = pd.read_csv('basic_data.csv')
df = dataset[['name']]
def uzyskajInformacje(zasob):
    url = "https://en.wikipedia.org/wiki/"
    if " " in zasob:
        zasob = zasob.replace(" ", "_")
    newUrl = url + zasob
    print(newUrl)
    page = urlopen(newUrl)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find(id="firstHeading")
    newText = soup.find(id="mw-content-text").find_all("p")
    textList=[]
    for row in title:
        title = row.text
    for row in newText:
        newRow = row.text.replace('\n', '')
        newRow = newRow.replace('[1]', '')
        newRow = newRow.replace('[2]', '')
        newRow = newRow.replace('[3]', '')
        newRow = newRow.replace('[4]', '')
        newRow = newRow.replace('[', '')
        newRow = newRow.replace(']', '')
        newRow = newRow.replace("'", '')
        textList.append(newRow)

    return title, textList

def getPlainVocabulary():
    names = [word_tokenize(name['name']) for index, name in df.iterrows()]
    mergeNames = list(itertools.chain.from_iterable(names))
    plainvocabulary = list(set(mergeNames))
    return plainvocabulary

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]
def spelling_correction(name):
    splittedName = word_tokenize(name)
    vocwords = list(itertools.chain.from_iterable([getPlainVocabulary()]))
    for i,word in enumerate(splittedName):
        if (word not in vocwords and not word.isdigit()): # ignore digits
            levdistances = []
            for vocword in vocwords:
                levdistances.append(levenshtein_distance(word,vocword))
            splittedName[i] = vocwords[levdistances.index(min(levdistances))]
        else:
            splittedName[i] = word
    return ' '.join(splittedName)
def checkSpelling(gra):
    wlasciweSlowo = spelling_correction(gra)
    print(wlasciweSlowo)
    if gra == wlasciweSlowo:
        return gra
    else:
        return wlasciweSlowo