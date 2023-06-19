import os
from googleapiclient.discovery import build
import isodate
import json


class Channel:
    API_KEY = os.getenv('API_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    """Класс для ютуб - канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
    Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))
