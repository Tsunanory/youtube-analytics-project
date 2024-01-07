import json
import os
from googleapiclient.discovery import build
api_key: str = os.getenv('YOUTUBE_API_KEY')


class Channel:

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        youtube = build('youtube', 'v3', developerKey=api_key)
        self.channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self._channel_id
        self.subscribers_count = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_count = self.channel['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self._channel_id

    @staticmethod
    def printj(dict_to_print: dict) -> None:
        """Выводит словарь в json-подобном удобном формате с отступами"""
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

    def print_info(self, channel_id) -> None:
        """Выводит в консоль информацию о канале."""
        self.printj(self.channel)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, json_name):
        dict_for_jsonisation = {'channel_id': self.channel_id,
                                'title': self.title,
                                'description': self.description,
                                'url': self.url,
                                'subscribers_count': self.subscribers_count,
                                'video_count': self.video_count,
                                'views_count': self.view_count,
                                }
        with open(json_name, 'w') as file:
            json.dump(dict_for_jsonisation, file)
