import books_preprocessing
from newsdata import get_top_news_matches
from youtubesearch import search_videos
from sentence_transformers import SentenceTransformer

from flask import Flask, request, jsonify
app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_work():
    data = request.get_json()
    user_input = data['query']

# takes in user input
    input = model.encode(user_input)

    videos = search_videos(input)
    news = get_top_news_matches(input)


    return jsonify({
        'books': books,
        'videos': videos,
        'news': news
    })

app.run(port=5000)