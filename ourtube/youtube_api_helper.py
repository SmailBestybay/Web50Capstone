from urllib.error import HTTPError
from googleapiclient.discovery import build
from django.conf import settings

_youtube = build(
    settings.API_SERVICE_NAME,
    settings.API_VERSION,
    developerKey=settings.GOOGLE_API_KEY
    )

def search(query):
    '''Search for a youtube channel'''

    response = _youtube.search().list(
        part='snippet',
        q=query,
        type='channel'
    ).execute()

    return response['items']

def get_videos(channel):
    '''Get last 3 videos from playlist'''
    
    response = _youtube.playlistItems().list(
        part='snippet',
        playlistId=channel.playlist_id,
        maxResults=3,
    ).execute()

    return response['items']
