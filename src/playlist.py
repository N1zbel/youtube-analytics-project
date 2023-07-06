from datetime import timedelta
from src.channel import Channel
import os


class PlayList:
    api_key = os.getenv('API_YOUTUBE')

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = None
        self.url = None
        self.videos = []
        self.video_data()

    def video_data(self):
        youtube = Channel.get_service().playlistItems().list(
            playlistId=self.playlist_id,
            part='snippet,contentDetails,id,status',
            maxResults=10,
        ).execute()
        playlist_data = youtube.get('items')[0]
        self.title = playlist_data.get('snippet').get('title').split(".")[0]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        video_ids = [video['contentDetails']['videoId'] for video in youtube['items']]
        videos = Channel.get_service().videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()
        self.videos = videos.get('items')

    @property
    def total_duration(self):
        total = timedelta()
        for video in self.videos:
            duration = video.get('contentDetails').get('duration')
            video_duration = self.new_duration(duration)
            total += video_duration
        return total

    @staticmethod
    def new_duration(duration):
        parts = duration[2:]
        if 'M' in parts:
            minutes = parts.split('M')
            minutes = int(minutes[0])
        else:
            minutes = 0
        if 'S' in parts:
            seconds = parts.split('M')
            seconds = int(seconds[1][:-1])
        else:
            seconds = 0
        video_duration = timedelta(minutes=minutes, seconds=seconds)
        return video_duration

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video.get('statistics').get('likeCount'))
        return f"https://youtu.be/{best_video['id']}"
