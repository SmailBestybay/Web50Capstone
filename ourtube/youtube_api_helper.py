from googleapiclient.discovery import build
from django.conf import settings

_youtube = build(
    settings.API_SERVICE_NAME,
    settings.API_VERSION,
    developerKey=settings.GOOGLE_API_KEY
)

def yt_search(query):
    '''Search for a youtube channel'''

    response = _youtube.search().list(
        part='snippet',
        q=query,
        type='channel'
    ).execute()


    return response['items']

def get_channel_uploads_id(channel_id):
    '''Get uploads id for the given channel'''

    response = _youtube.channels().list(
        part='contentDetails',
        id=channel_id
    ).execute()

    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def get_videos(channel):
    '''Get last 3 videos from playlist.
    Returns an array of youtube video ids
    '''
    
    response = _youtube.playlistItems().list(
        part='snippet',
        playlistId=channel.playlist_id,
        maxResults=3,
    ).execute()
    video_ids = []
    for item in response['items']:
        video_ids.append(item['snippet']['resourceId']['videoId'])
    return video_ids
