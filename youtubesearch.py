from dotenv import load_dotenv
import os
from googleapiclient.discovery import build 


# search and then puts the results into a list
def search_videos(input):
    
    # load api
    load_dotenv('api.env')
    youtube_api = os.getenv('YOUTUBE_API_KEY')

    # https://developers.google.com/youtube/v3/docs
    youtube = build('youtube', 'v3', developerKey=youtube_api)


    request = youtube.search().list(
        q=input, # what you search for
        part='snippet', # title, descp, thumbnails, channel, publish date
        type='video',
        maxResults=3 # provide 3 top results
    )
    response = request.execute()

    results_list = []

    with open('recommended_videos.txt', 'a', encoding='utf-8') as file: 
        file.write('\n\nNEW RUN:\n')
        file.write(f'Results for: {input}\n\n')

        # looks through the results in key items
        # then clicks into the snippet and in there obtains title
        # then clicks into another part called id and obtains the videoid
        for result in response['items']:
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

            results_list.append(video_dict)

    return results_list

# search_videos('australia economy')
 