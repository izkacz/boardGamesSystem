from urllib.request import urlopen
import os
from nltk import word_tokenize
import itertools
import pandas as pd
import requests
from bs4 import BeautifulSoup
import random

def uzyskajInformacje(zasob):
    url = "https://pl.wikipedia.org/wiki/"
    if " " in zasob:
        zasob = zasob.replace(" ", "_")
    newUrl = url + zasob
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
    sentencess = [word_tokenize(sentence['Sentence']) for index, sentence in sentences_df.iterrows()]
    mergesentences = list(itertools.chain.from_iterable(sentencess))
    plainvocabulary = list(set(mergesentences))
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
def spelling_correction(sentence):
    splittedsentence = word_tokenize(sentence)
    vocwords = list(itertools.chain.from_iterable([getPlainVocabulary()]))
    for i,word in enumerate(splittedsentence):
        if (word not in vocwords and not word.isdigit()): # ignore digits
            levdistances = []
            for vocword in vocwords:
                levdistances.append(levenshtein_distance(word,vocword))
            splittedsentence[i] = vocwords[levdistances.index(min(levdistances))]
        else:
            splittedsentence[i] = word
    return ' '.join(splittedsentence)