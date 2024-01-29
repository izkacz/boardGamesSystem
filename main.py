import json

from flask import Flask, redirect, url_for, request, Response, jsonify, render_template
import csv

from gameInfo import uzyskajInformacje, checkSpelling
from recommendation import genre_choosing

app = Flask(
  __name__,
  template_folder='htmlTemplates'
)

@app.route("/")
def hello():
    return render_template('welcomePage.html')

@app.errorhandler(404)
def notFound(error=None):
    message = {
        'status': 404,
        'message': 'Not found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.route("/makeWishlist")
def wishList():
    return render_template('makeWishlist.html')

@app.route("/recommendation")
def rekomendacja():
    return render_template('recommendation.html')

@app.route("/searchGames", methods=['GET','POST'])
def poszukajGry():
        return render_template('searchGames.html')

@app.route("/genreRecommendation", methods=['GET','POST'])
def rekomendacjaPoGatunku():
    if request.method == 'GET':
       genre = request.args.get('genre')
       games = genre_choosing(genre)
       return render_template('genreRecommendation.html', games=games)
    else:
        return render_template('genreRecommendation.html')

# @app.route("/artistRecommendation", methods=['POST'])
# def rekomendacjaPoArtyscie():
#     return render_template('artistRecommendation.html')

@app.route("/gameRecommendation", methods=['POST'])
def rekomendacjaPoGrze():
    return render_template('gameRecommendation.html')

@app.route("/gameInfo", methods=['GET','POST'])
def informacjeOGrze():
    if request.method == 'POST':
       zasob = request.form.get('zasob')
       slowo = checkSpelling(zasob)
       if slowo == zasob:
          title, text = uzyskajInformacje(zasob)
          return render_template('gameWikiInfo.html', title=title, text=text)
       else:
           return render_template('gameWikiInfo.html', slowo=slowo)
    else:
       return render_template('gameWikiInfo.html')

