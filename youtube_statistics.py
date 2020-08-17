import requests
import json
from tqdm import tqdm

class YTstats:
    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        # self.channel_uname = channel_uname
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        # print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            print(data)
            data = data['items'][0]['statistics']
        except:
            data = None
        
        self.channel_statistics = data
        return data

    def get_channel_video_data(self):
        # Video ids
        channel_videos = self._get_channel_videos(limit=50)
        print(len(channel_videos))

        # Video statistics
        
        for video_id in tqdm(channel_videos):
            data = self._get_single_video_data(video_id)
            channel_videos[video_id].update(data)

        self.video_data = channel_videos
        return channel_videos

    def _get_single_video_data(self, video_id):
        url = self._create_single_video_data_url(video_id)
        
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            print(url)
            data = data['items'][0]
        except:
            print('error')
            data = dict()

        return data

    # TODO: Keep working on creating a single url for our api call. Reached daily query quota.
    def _create_single_video_data_url(self, video_id):
        # To reduce api calls, don't create a new url for each part.
        # Instead add all parts to the same url as youtube api allows by looping through them
        parts = ['snippet', 'statistics', 'contentDetails']
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key{self.api_key}&part={parts.index(0)}&part={parts.index(1)}&part={parts.index(2)}'
        return url

    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?part=id&channelID={self.channel_id}&order=date&key={self.api_key}'
        if limit is not None and isinstance(limit, int):
            url += '&maxResults=' +str(limit)
        
        # Creates a vid dictionary (npt = self._get_channel_videos_per_page(url))
        vid, npt = self._get_channel_videos_per_page(url)
        index = 0
        while(npt is not None and index < 10):
            nexturl = url + '&pageToken=' + npt
            next_vid, npt = self._get_channel_videos_per_page(nexturl)
            vid.update(next_vid)
            index += 1
        
        return vid

    def _get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        # Create an empty dictionary named channel_videos
        channel_videos = dict()

        # If 'items' does not exist in response, return a dictionary of none - {None}
        if 'items' not in data:
            return channel_videos, None

        # Store 'items' section of the response in item_data variable
        item_data = data['items']
        # Store the 'nextPageToken' in a local variable so that we can iterate through all response pages
        nextPageToken = data.get('nextPageToken', None)
        # Iterate through each item in item_data
        for item in item_data:
            try:
                # Store the 'kind' of each video in a variable
                kind = item['id']['kind']
                if kind == 'youtube#video':     # We only want youtube videos, not playlists or other types
                    # Store the id of each video in local variable
                    video_id = item['id']['videoId']
                    # Add video_id as key in channel_videos dictionary which has a value of an empty dictionary
                    # Example output: {'video_id_1': {}, 'video_id_2': {}, 'video_id_3': {}} 
                    channel_videos[video_id] = dict()
            except KeyError:
                print('key error')

        # Return the channel_videos dictionary as well as the next page token that we need to retrieve next set of results
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
        
        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(' ', '_').lower()
        file_name = channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print('file dumped')