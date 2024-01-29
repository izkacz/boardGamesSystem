from urllib.request import urlopen

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
