from booksearch import get_top_3_book_groups
from newsdata import get_top_news_matches
from youtubesearch import search_videos
from flask import Flask, request, jsonify
from flask_cors import CORS

# user_input = 'trump'

# videos = search_videos(user_input)
# news = get_top_news_matches(user_input)
# books = get_top_3_book_groups(user_input)

# print('Videos')
# print(videos)
# print()
# print("news")
# print(news)
# print()
# print("books")
# print(books)
 
app = Flask(__name__)
CORS(app, resources = {
    r"/api/*": {
        "origin": ["http://localhost:5173"],
        "methods": ["GET", "POST"],
        "allows_headers": ["Content-Type"]
    }
})

@app.route('/api/recommend', methods=['POST'])
def recommend_work():
    data = request.get_json()
    user_input = data.get('query', '')

    if not user_input:
        return jsonify({'error': 'no input provided'}, 400)

    try: 
        videos = search_videos(user_input)
        news = get_top_news_matches(user_input)
        books = get_top_3_book_groups(user_input)


        return jsonify({
            'books': books,
            'videos': videos,
            'articles': news
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods = ['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
