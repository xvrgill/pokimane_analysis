import requests
import json
from tqdm import tqdm

class YTstats:
    def __init__(self, api_key, channel_uname):
        self.api_key = api_key
        self.channel_uname = channel_uname
        self.channel_id = None
        self.channel_statistics = None
        # Stores all video statistics
        self.video_data = None

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername={self.channel_uname}&key={self.api_key}'
        # print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            c_id = data['items'][0]['id']
        except:
            c_id = None
        try:
            stats = data['items'][0]['statistics']
        except:
            stats = None
        self.channel_id = c_id
        self.channel_statistics = stats
        return stats, c_id

    def get_channel_video_data(self):
        # Video ids
        # YouTube Data v3 api only allows for a maximum of 50 results to be returned at once
        # Manual pagination is required after this point. We will do this with the provided nextPageToken
        channel_videos = self._get_channel_videos(limit=50)
        # Video statistics
        parts = ['snippet', 'statistics', 'contentDetails']
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)
        self.video_data = channel_videos
        return channel_videos

    def _get_single_video_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={self.api_key}&part={part}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except:
            print('error')
            data = dict()
        return data

    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?part=id&channelId={self.channel_id}&order=date&key={self.api_key}'
        if limit is not None and isinstance(limit, int):
            url += '&maxResults=' + str(limit)
        # Define both vid and npt variables simultaneously to result of _get_channel_videos_per_page(url) function
        # Remember that we return two variables in this function
        # vid = channel_videos and npt = nextPageToken
        vid, npt = self._get_channel_videos_per_page(url)
        # We need to loop through our results since the above function only returns one page of results
        # Create a loop that finds npt on each page until there is none
        # Set an index starting at 0
        index = 0
        # Use a while loop to continue the loop as long as a npt is found on a maximum of 10 pages
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
        # If 'items' does not exist in response, return the empty dictionary and None for the npt
        # This means that there were no search results
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
                    # Example output: { channel_videos:{'video_id_1': {}, 'video_id_2': {}, 'video_id_3': {}} }
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
        # How to get channel name from dictionary
        # Don't need since we modified code to have channel title as input
        # channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = self.channel_uname
        file_name = channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(fused_data, f, indent=4)
        print('file dumped')