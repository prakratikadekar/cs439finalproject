from dotenv import load_dotenv
import os
from googleapiclient.discovery import build 

load_dotenv('api.env')
youtube_api = os.getenv('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=youtube_api)


# search and then puts the results into a list
def search_videos(input):
    request = youtube.search().list(
        q=input, # what you search for
        part='snippet', # title, descp, thumbnails, channel, publish date
        type='video',
        maxResults=3 # provide 3 top results
    )
    response = request.execute()

    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoID']
        print(f'{title} - youtube.com/watch?v={video_id}')

            
search_videos('us economy')
