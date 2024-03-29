
import pandas as pd
from flask import Flask, request,  jsonify, render_template
from gameInfo import uzyskajInformacje, checkSpelling, makePrediction
from recommendation import genre_choosing, title_recommendation, description_recommendation, filter_recommendations

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


@app.route("/titleRecommendation")
def rekomendacjaPoTytule():
    if request.method == 'GET':
        title = request.args.get('title')
        games = title_recommendation(title)
        return render_template('recommendation.html', tables=[games.to_html(classes='data', index=False)], titles=games.columns.values, title=title)
    else:
        return render_template('recommendation.html')

@app.route("/recommendation", methods=['GET'])
def rekomendacja():
    return render_template('recommendation.html')

@app.route("/descriptionRecommendation")
def rekomendacjaPoOpisie():
    if request.method == 'GET':
        description = request.args.get('description')
        games = description_recommendation(description)
        return render_template('recommendation.html', tables=[games.to_html(classes='data', index=False)],
                               titles=games.columns.values, description=description)
    else:
        return render_template('recommendation.html')

@app.route("/filterRecommendations")
def filtrowanieRekomendacji():
    if request.method == 'GET':
        filtered_games = pd.DataFrame()
        filter = request.args.get('filter')
        description = request.args.get('hiddenDescription')
        title = request.args.get('hiddenTitle')
        genre = request.args.get('hiddenGenre')
        if title:
            games = title_recommendation(title)
            filtered_games = filter_recommendations(filter, games)
        elif description:
            games = description_recommendation(description)
            filtered_games = filter_recommendations(filter, games)
        elif genre:
            games = genre_choosing(genre)
            filtered_games = filter_recommendations(filter, games)
        return render_template('recommendation.html',
                               tables=[filtered_games.to_html(classes='data', index=False)],
                               titles=filtered_games.columns.values,
                               filter=filter,
                               title=title, description=description, genre=genre)
    else:
        return render_template('recommendation.html')

@app.route("/genreRecommendation", methods=['GET','POST'])
def rekomendacjaPoGatunku():
    if request.method == 'GET':
       genre = request.args.get('genre')
       games = genre_choosing(genre)
       return render_template('recommendation.html',
                               tables=[games.to_html(classes='data', index=False)],
                               titles=games.columns.values,
                               genre=genre)
    else:
        return render_template('recommendation.html')

@app.route("/gameInfo", methods=['GET','POST'])
def informacjeOGrze():
    if request.method == 'POST':
       zasob = request.form.get('zasob')
       slowo = checkSpelling(zasob)
       if slowo == zasob:
          title, text = uzyskajInformacje(zasob)
          genre=makePrediction(zasob)
          prawd = "This game probably belongs to genre: "
          inneGry = "Other games from the genre"
          return render_template('gameWikiInfo.html', title=title, text=text, genre=genre, prawd=prawd, inneGry=inneGry)
       else:
           mysl= "Did you mean: "
           return render_template('gameWikiInfo.html', mysl=mysl, slowo=slowo)
    else:
       return render_template('gameWikiInfo.html')
