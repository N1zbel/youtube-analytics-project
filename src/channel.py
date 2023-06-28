import os
from googleapiclient.discovery import build
import isodate
import json


class Channel:
    API_KEY = os.getenv('API_YOUTUBE')

    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
    Дальше все данные будут подтягиваться по API.
    Атрибуты:
        channel_id (str): Идентификатор канала.
        channel_title (str): Название канала.
        channel_description (str): Описание канала.
        channel_url (str): Ссылка на канал.
        channel_subs (int): Количество подписчиков канала.
        video_count (int): Количество видео на канале.
        chanel_views (int): Общее количество просмотров канала.
        """

        self.youtube = self.get_service()
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        channel_info = self.channel['items'][0]
        self.title = channel_info['snippet']['title']
        self.channel_description = channel_info['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.channel_subs = int(channel_info["statistics"]["subscriberCount"])
        self.video_count = channel_info["statistics"]["videoCount"]
        self.chanel_views = channel_info["statistics"]["viewCount"]

    def __str__(self):
        """
        Возвращает строковое название канала и ссылку на него
        """
        return f'{self.title, self.url}'

    def __add__(self, other):
        """
        Возвращает сумму подписчиков на 2х каналах
        """
        return self.channel_subs + other.channel_subs

    def __sub__(self, other):
        """
        Возвращает разность подписчиков на 2х каналах
        """
        return self.channel_subs - other.channel_subs

    def __gt__(self, other):
        """
        проверяет больше ли подписчиков на первом канале относительно второго
        возвращает bool значение True если больше, False если меньше
        """
        return self.channel_subs > other.channel_subs

    def __ge__(self, other):
        """
        проверяет больше или столько же подписчиков на первом канале относительно второго
        возвращает bool значение True если больше или равно, False если меньше
        """
        return self.channel_subs >= other.channel_subs

    def __lt__(self, other):
        """
        проверяет меньше ли подписчиков на первом канале относительно второго
        возвращает bool значение True если меньше, False если больше
        """
        return self.channel_subs < other.channel_subs

    def __le__(self, other):
        """
        проверяет меньше или равно подписчиков на первом канале относительно второго
        возвращает bool значение True если меньше или равно, False если больше
        """
        return self.channel_subs <= other.channel_subs

    def __eq__(self, other):
        """
        проверяет равенство подписчиков на 2х каналах
        возвращает bool значение True если равно, False если не равно
        """
        return self.channel_subs == other.channel_subs

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
