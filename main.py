from booksearch import get_top_3_book_groups
from newsdata import get_top_news_matches
from youtubesearch import search_videos

from flask import Flask, request, jsonify
app = Flask(__name__)


def recommend_work():
    data = request.get_json()
    user_input = data['query']

    videos = search_videos(user_input)
    news = get_top_news_matches(user_input)
    books = get_top_3_book_groups(user_input)


    return jsonify({
        'books': books,
        'videos': videos,
        'news': news
    })

app.run(port=5000)