import os
import re
import json
from .video import Video
from .video import PLVideo
from .channel import Channel
from datetime import timedelta
from googleapiclient.discovery import build
api_key: str = os.getenv('YOUTUBE_API_KEY')

class PlayList(PLVideo, Channel, Video):

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='snippet,contentDetails',
                                                     maxResults=50,
                                                     ).execute()
        self.videos = []
        self.video_ids = [video['snippet']['resourceId']['videoId'] for
                       video in self.playlist['items']]
        for video_id in self.video_ids:
            video = youtube.videos().list(id=video_id,
                    part='contentDetails,statistics').execute()
            self.videos.append(video)

        self.video_durations = []
        for video in self.videos:
            self.video_durations.append(video['items'][0]['contentDetails']['duration'])
        self._channel_id = self.playlist['items'][0]['snippet']['channelId']
        self.all_playlists = youtube.playlists().list(channelId=self._channel_id,
                                                      part='contentDetails,snippet',
                                                      maxResults=50,
                                                      ).execute()
        self.pls = json.dumps(self.all_playlists['items'], indent=4, sort_keys=True)
        self.title = [pl['snippet']['title'] for pl in self.all_playlists['items']
                      if pl['id'] == self.playlist_id][0]
        self.url = "https://www.youtube.com/playlist?list=" + self.playlist_id

    @property
    def total_duration(self):
        res = timedelta()
        for duration in self.video_durations:
            match = re.match(r'PT(\d+)M(\d+)?S?', duration)
            minutes = int(match.group(1))
            seconds = int(match.group(2)) if match.group(2) else 0
            res += timedelta(minutes=minutes, seconds=seconds)
        return res

    def show_best_video(self):
        likes = []
        ind = 0
        ind2 = 0
        result = 'https://youtu.be/'
        for video in self.videos:
            likes.append(video['items'][0]['statistics']['likeCount'])
        for video in self.videos:
            if video['items'][0]['statistics']['likeCount'] == max(likes):
                result += video['items'][ind]['id']
        return result

