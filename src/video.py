import json
import os
from googleapiclient.discovery import build
api_key: str = os.getenv('YOUTUBE_API_KEY')


class Video:

    def __init__(self, video_id):
        self.video_id = video_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video = youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + video_id
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title

class PLVideo:
    def __init__(self, video_id, playlist_id):
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.video = youtube.videos().list(id=video_id, part='snippet,statistics,contentDetails').execute()
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + video_id
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']
        self.playlist_id = playlist_id

    def __str__(self):
        return self.video_title


# youtube = build('youtube', 'v3', developerKey=api_key)
# video = youtube.videos().list(id='AWX4JnAnjBE', part='snippet,statistics,contentDetails').execute()
# print(video)