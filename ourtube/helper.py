from googleapiclient.discovery import build
from django.conf import settings
from .models import Feed

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

def get_feeds(current_user):
    """Get the feeds that current user owns or follows. 
    Additionally, set user object on owner attribute for each feed
    """
    feeds = Feed.objects.all().filter(members__id=current_user.id)
    for feed in feeds:
        feed.owner = feed.membership_set.filter(is_owner=True).first().user
    return feeds
