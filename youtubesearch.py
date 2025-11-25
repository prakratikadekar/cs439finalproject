from dotenv import load_dotenv
import os

load_dotenv('api.env')
youtube_api = os.getenv('YOUTUBE_API_KEY')
