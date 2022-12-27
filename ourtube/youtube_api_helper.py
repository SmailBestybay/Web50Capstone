from urllib.error import HTTPError
from googleapiclient.discovery import build
from django.conf import settings

_youtube = build(
    settings.API_SERVICE_NAME,
    settings.API_VERSION,
    developerKey=settings.GOOGLE_API_KEY
    )

# search method



# def get_uploads(channel_id):
#     channels_response = _youtube.channels().list(
#         # Channel id, forUsername or mine(for my channel's video).
#         id=channel_id,
#         part='contentDetails'
#     ).execute()
#     for channel in channels_response['items']:
#         return channel['contentDetails']['relatedPlaylists']['uploads']
#     return None

def get_videos(channel):
    '''Get last 3 videos from playlist
    '''
    
    response = _youtube.playlistItems().list(
        part='snippet',
        playlistId=channel.playlist_id,
        maxResults=3,
    ).execute()

    return response['items']


##################################

# API_KEY = ''
# # This is San Diego Python's YouTube channel id
# CHANNEL_ID = 'UCXU-oZwaHnoYUhja_yrrrGg'
# # How many videos do you want to show
# LAST_VIDEOS_NR = 4

# def authenticate():
#     return build('youtube', 'v3', developerKey=API_KEY)


# def get_uploads():
#     channels_response = youtube.channels().list(
#         # Channel id, forUsername or mine(for my channel's video).
#         id=CHANNEL_ID,
#         part='contentDetails'
#     ).execute()
#     for channel in channels_response['items']:
#         return channel['contentDetails']['relatedPlaylists']['uploads']
#     return None


# def list_uploaded_videos(uploads_play_list_id):
#     # Retrieve the list of uploaded videos.
#     play_list_request = youtube.playlistItems().list(
#         playlistId=uploads_play_list_id,
#         part='snippet'
#     )
#     while play_list_request:
#         play_list_response = play_list_request.execute()
#         for playlist_item in play_list_response['items']:
#             if playlist_item['snippet']['position'] <= LAST_VIDEOS_NR:
#                 video_nr = playlist_item['snippet']['position']
#                 title = playlist_item['snippet']['title']
#                 description = playlist_item['snippet']['description']
#                 datetime_published = playlist_item['snippet']['publishedAt']
#                 thumbnail = playlist_item['snippet']['thumbnails']['standard']['url']
#                 video_id = playlist_item['snippet']['resourceId']['videoId']
#                 print(
#                     f'Video nr: {video_nr + 1}\n'
#                     f'Title: {title}\n'
#                     f'Description: {description}\n'
#                     f'Published date: {datetime_published}\n'
#                     f'Thumbnail: {thumbnail}\n'
#                     f'Url: https://www.youtube.com/watch?v={video_id}\n'
#                 )
#         # next page
#         play_list_request = youtube.playlistItems().list_next(
#             play_list_request, play_list_response)


# if __name__ == '__main__':
#     youtube = authenticate()
#     try:
#         uploads_playlist_id = get_uploads()
#         if uploads_playlist_id:
#             list_uploaded_videos(uploads_playlist_id)
#         else:
#             print('There are not any uploaded videos in this channel.')
#     except HTTPError as e:
#         print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')