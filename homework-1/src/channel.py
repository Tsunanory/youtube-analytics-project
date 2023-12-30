from googleapiclient.discovery import build
import json
import os

class Channel:
    api_key: str = os.getenv('YOUTUBE_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id):
        self.channel_id = channel_id

    def print_info(self, to_print):
        print(json.dumps(to_print, indent=2, ensure_ascii=False))

    channel = youtube.channels().list(self.channel_id, part='snippet').execute()
