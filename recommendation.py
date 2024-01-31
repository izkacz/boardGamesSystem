import pandas as pd
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def genre_choosing(genre):
    df = pd.read_csv('categories_data.csv')
    df.columns = df.columns.str.lower()
    df2 = pd.read_csv('basic_data.csv')
    genre = genre.lower()
    gamesVotes = []
    gamesIndecies = []
    for index, row in df.iterrows():
        if row[genre] == 1:
            gamesVotes.append(row['bayes_rating'])
            if len(gamesVotes) == 7:
                break
    for vote in gamesVotes:
        for index, row in df2.iterrows():
            if row['bayes_rating'] == vote:
                gamesIndecies.append(index)
    games = df2.iloc[gamesIndecies][['name', 'description']]
    games['description'] = games['description'].str.replace('<br/>', ' ')
    games.rename(columns={'name': 'Tytuł', 'description': 'Opis'}, inplace=True)
    return games

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

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return str(text).translate(translator)

def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def title_recommendation(title):
    df = pd.read_csv('basic_data.csv')

    test_data = remove_punctuation(title.lower())
    test_df = pd.DataFrame({'name': [test_data]})
    train_data = df['name'].str.lower().apply(remove_punctuation)
    train_data = pd.concat([train_data, test_df['name']], ignore_index=True)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(train_data)

    test_index = len(train_data) - 1
    jaccard_similarities = []

    for i in range(test_index):
        set1 = set(tfidf_matrix[test_index].nonzero()[1])
        set2 = set(tfidf_matrix[i].nonzero()[1])
        jaccard_sim = jaccard_similarity(set1, set2)
        jaccard_similarities.append(jaccard_sim)

    recommendations_indices = sorted(range(len(jaccard_similarities)), key=lambda i: jaccard_similarities[i],
                                     reverse=True)

    recommended_list = []
    unique_recommendations = []
    for index in recommendations_indices:
        recommended_description = df.loc[index, 'name']
        if recommended_description not in recommended_list:
            recommended_list.append(recommended_description)
            unique_recommendations.append(index)
            if len(unique_recommendations) == 7:
                break

    recommended_games = df.iloc[unique_recommendations][['name', 'description']]
    recommended_games['description'] = recommended_games['description'].str.replace('<br/>', ' ')
    recommended_games.rename(columns={'name': 'Tytuł', 'description': 'Opis'}, inplace=True)
    return recommended_games


def description_recommendation(description):
    df = pd.read_csv('basic_data.csv')

    test_data = remove_punctuation(description.lower())
    test_df = pd.DataFrame({'description': [test_data]})
    train_data = df['description'].str.lower().apply(remove_punctuation)
    train_data = pd.concat([train_data, test_df['description']], ignore_index=True)

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(train_data)

    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    recommendations_indices = cosine_similarities.argsort()[0][::-1]

    recommended_list = []
    unique_recommendations = []
    for index in recommendations_indices:
        recommended_description = df.loc[index, 'description']
        if recommended_description not in recommended_list:
            recommended_list.append(recommended_description)
            unique_recommendations.append(index)
            if len(unique_recommendations) == 7:
                break

    recommended_games = df.iloc[unique_recommendations][['name', 'description']]
    recommended_games['description'] = recommended_games['description'].str.replace('<br/>', ' ')
    recommended_games.rename(columns={'name': 'Tytuł', 'description': 'Opis'}, inplace=True)
    return recommended_games

def filter_recommendations(filter, games):
    regexp = re.compile(r'(?i){}'.format(re.escape(filter)))
    def pattern_match(value):
        return bool(re.search(regexp, str(value)))

    matching_rows = games.applymap(pattern_match)
    matching_indecies = matching_rows.index[matching_rows.any(axis=1)].tolist()
    filtered_games = games.loc[matching_indecies]
    return filtered_games
