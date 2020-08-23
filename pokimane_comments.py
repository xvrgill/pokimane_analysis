import requests
import json
from tqdm import tqdm

# Returning 'data is none'
# TODO: Try again later once api quota is reset

class PokimaneComments:
    def __init__(self, api_key, channel_uname):
        self.api_key = api_key
        self.channel_uname = channel_uname
        self.channel_statistics = None
        self.channel_id = None
        self.video_data = None
        self.comment_data = None

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={self.channel_uname}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            c_id = data['items'][0]['id']
        except:
            print('error setting channel id')
            c_id = None
        try:
            stats = data['items'][0]['statistics']
            print(stats)
        except:
            print('error getting channel statistics')
            stats = None
        self.channel_id = c_id
        self.channel_statistics = stats
        return stats, c_id

    def get_channel_video_data(self):
        # Video IDs
        channel_videos = self._get_channel_videos(limit=50)

        # Video Statistics
        parts = ['snippet', 'statistics', 'contentDetails']
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
            comment_data = self._get_single_video_comment_data(video_id, limit=100)
            channel_videos[video_id]['comment_threads'].update(comment_data)
        
        self.video_data = channel_videos
        return channel_videos
    
    def _get_single_video_comment_data(self,video_id, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={self.api_key}&videoId={video_id}&part=replies&part=snippet'
        if limit is not None and isinstance(limit, int):
            url += '&maxResults=' + limit
        com, npt = self._get_comments_per_page(url)
        index = 0
        while(npt is not None):
            nexturl = url + '&pageToken=' + npt
            next_comment, npt = self._get_comments_per_page(nexturl)
            com.update(next_comment)
            index += 1
        return com


    def _get_comments_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        comments = dict()
        if 'items' not in data:
            return comments, None
        item_data = data['items']
        nextPageToken = data.get('nextPageToken', None)
        for item in item_data:
            try:
                kind = item['kind']
                if kind == 'youtube#commentThread':
                    thread_id = item['id']
                    comments[thread_id] = dict()
            except KeyError:
                print('key error while setting thread id')
        return comments, nextPageToken


    def _get_single_video_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={self.api_key}&part={part}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except:
            print('error getting single video data')
            data = dict()
        return data

    def _get_channel_videos(self, limit = None):
        url = f'https://www.googleapis.com/youtube/v3/search?part=id&channelId={self.channel_id}&order=date&key={self.api_key}'
        if limit is not None and isinstance(limit, int):
            url += '&maxResults=' + str(limit)
        vid, npt = self._get_channel_videos_per_page(url)
        # loop through pages
        index = 0
        while (npt is not None and index < 20):
            nexturl = url + '&pageToken' + npt
            nextvid, npt = self._get_channel_videos_per_page(nexturl)
            vid.update(nextvid)
            index += 1
        return vid

    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        if 'items' not in data:
            return channel_videos, None
        item_data = data['items']
        nextPageToken = data.get('nextPageToken', None)
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print('key error')
        return channel_videos, nextPageToken

    def dump(self):
        if self.channel_statistics is None or self.video_data is None:
            print('data is none')
            return
        fused_data = {
            self.channel_id: {
                'channel_statistics': self.channel_statistics,
                'video_data': self.video_data
            }
        }
        # How to get channel name from dictionary
        # Don't need since we modified code to have channel title as input
        # channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = self.channel_uname
        file_name = channel_title + '_comments.json'
        with open(file_name, 'w') as f:
            json.dump(fused_data, f, indent=4)
        print('file dumped')

        