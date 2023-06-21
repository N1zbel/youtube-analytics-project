import os
from googleapiclient.discovery import build
import isodate
import json


class Channel:
    API_KEY = os.getenv('API_YOUTUBE')


    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
    Дальше все данные будут подтягиваться по API."""
        self.youtube = self.get_service()
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.channel_description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.channel_subs = self.channel['items'][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel['items'][0]["statistics"]["videoCount"]
        self.chanel_views = self.channel['items'][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def to_json(self, filename):
        channel_data = {
            'channel_id': self.channel_id,
            'channel_title': self.title,
            'channel_description': self.channel_description,
            'channel_url': self.url,
            'subscriberCount': self.channel_subs,
            'videoCount': self.video_count,
            'viewCount': self.chanel_views
        }
        with open(filename, 'w') as file:
            json.dump(channel_data, file)
