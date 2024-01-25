from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup
import random

def uzyskajInformacje(zasob):
    url = "https://en.wikipedia.org/wiki/"
    if " " in zasob:
        zasob = zasob.replace(" ", "_")
    newUrl = url + zasob
    response = requests.get(newUrl)
    page = urlopen(newUrl)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    print(soup.prettify())
    title = soup.find(id="firstHeading")
    text = soup.find(id="mw-content-text")
    for row in title:
        title = row.text
    newText=[]
    for row in text:
        newText.append(row.text)
    print(title)
    print(newText)
    # text = text.splitlines()
    return title,newText