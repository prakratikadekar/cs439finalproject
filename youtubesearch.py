from dotenv import load_dotenv
import numpy as np
import os
from googleapiclient.discovery import build

print('before import sentence')
from sentence_transformers import SentenceTransformer

print('before model')
model = SentenceTransformer('all-MiniLM-L6-v2')
print('after model')


# search and then puts the results into a list
def search_videos(input):
    print(" ---- IN YOUTUBE ----")
    # load api
    load_dotenv('api.env')
    youtube_api = os.getenv('YOUTUBE_API_KEY')

    # https://developers.google.com/youtube/v3/docs
    youtube = build('youtube', 'v3', developerKey=youtube_api)

    video_categories = ['25', '28'] # according to api these numbers indicate politics and tech/cs specifically

    for category in video_categories:
        request = youtube.search().list(
            q=input, # what you search for
            part='snippet', # title, descp, thumbnails, channel, publish date
            type='video',
            maxResults=5, # extended to 5 and remove youtube shorts
            videoCategoryId = category
        )
        response = request.execute()

    orig_results = []
    with open('recommended_videos.txt', 'a', encoding='utf-8') as file: 
        file.write('\n\nNEW RUN:\n')
        file.write(f'Results for: {input}\n\n')

        # looks through the results in key items
        # then clicks into the snippet and in there obtains title
        # then clicks into another part called id and obtains the videoid
        for result in response['items']:
            if len(orig_results) == 3:
                break

            # checking if this is a yt short -> if yes discard
            if result['id']['kind'] != 'youtube#video':
                continue
            title = result['snippet']['title']
            video_id = result['id']['videoId']
            channel = result['snippet']['channelTitle']
            description = result['snippet']['description']

            file.write(f'{title} - youtube.com/watch?v={video_id}\n')
            video_link = f'https://youtube.com/watch?v={video_id}'

            video_dict = {
                'title': title,
                'channel': channel,
                'description': description,
                'url': video_link
            }

            orig_results.append(video_dict)
    
    
    if not orig_results:
        return []        
    
    
    input_embedding = model.encode(input)

    filtered_results = []

    for video in orig_results: 
        video_text = video['title'] + ' ' + video['description']
        embedded_video_text = model.encode(video_text)

        input_embedding = np.atleast_2d(input_embedding)
        embedded_video_text = np.atleast_2d(embedded_video_text)
        
        user_input_normalized = input_embedding / np.linalg.norm(input_embedding, axis=1, keepdims=True)
        embedded_video_text = embedded_video_text / np.linalg.norm(embedded_video_text, axis=1, keepdims=True) # 1 dimension across all articles (rows)

    
        similarities = np.dot(user_input_normalized, embedded_video_text.T)


        print('video similarity: ', similarities)
        # this value generally worked the best
        if similarities >= 0.7:
            video['similarity'] = similarities
            filtered_results.append(video)


    filtered_results.sort(key=lambda vid: vid['similarity'], reverse=True)
    return filtered_results[:3] # top 3 