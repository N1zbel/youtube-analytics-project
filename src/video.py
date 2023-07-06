from src.channel import Channel


class Video:
    def __init__(self, video_id):
        """Экземпляр инициализирует id видео.
        Атрибуты:
        video_id (str): Идентификатор видео.
        title (str): Название видео.
        url (str): URL-адрес видео.
        view_count (int): Количество просмотров видео.
        like_count (int): Количество лайков видео.
        """
        youtube = Channel.get_service().videos().list(
            part='snippet,statistics', id=video_id
        ).execute()
        video_data = youtube.get('items')[0]
        self.video_id = video_id
        self.title = video_data.get('snippet').get('title')
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = int(video_data.get('statistics').get('viewCount'))
        self.like_count = int(video_data.get('statistics').get('likeCount'))

    def __str__(self) -> str:
        """Возврат строкового значения названия канала"""
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """инициализирует экземляр класса
        video_id (str): Идентификатор видео.
        playlist_id (str): Идентификатор плейлиста."""
        super().__init__(video_id)
        self.playlist_id = playlist_id
