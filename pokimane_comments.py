import requests
import json
from tqdm import tqdm

class YTcomments:
    def __init__(self, api_key):
        self.api_key = api_key
        self.video_dictionary = None

    def read_channel_data(self):
        with open('pokimane.json', 'r') as f:
            channel_data = json.load(f)
        video_dictionary = self._create_video_id_object(channel_data)
        video_data = channel_data['UChXKjLEzAB1K7EZQey7Fm1Q']['video_data']
        for video in video_data:
            video_dictionary.update({video:[]})
        return video_dictionary

    def get_all_comments(self):
        video_dictionary = self.read_channel_data()
        for video_id in tqdm(video_dictionary):
            comments = self._get_comments(video_id)
            video_dictionary[video_id].append(comments)
        self.video_dictionary = video_dictionary
        return video_dictionary

    def _create_video_id_object(self, data):
        video_id_object = dict()
        return video_id_object

    def _get_comments (self, video_id):
        url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={self.api_key}&videoId={video_id}&part=snippet&part=replies&maxResults=100'
        comments, npt = self._get_comments_per_page(url)
        while (npt is not None):
            next_url = url +'&pageToken=' + npt
            next_comments, npt = self._get_comments_per_page(next_url)
            comments.append(next_comments)
        return comments   

    def _get_comments_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        comments = []
        if 'items' not in data:
            return comments, None
        item_data = data['items']
        nextPageToken = data.get('nextPageToken', None)
        for item in item_data:
            collection = dict()
            snippet = item['snippet']
            try:
                replies = item['replies']
            except:
                replies = None

            fused_data = {
                'snippet': snippet,
                'replies': replies
            }

            collection.update(fused_data)
            comments.append(collection)
        return comments, nextPageToken

    def dump(self):
        if self.video_dictionary is None:
            print('data is none')
            return
        final_data = self.video_dictionary
        file_name = 'video_comments.json'
        with open(file_name, 'w') as f:
            json.dump(final_data, f, indent=4)
        print('file dumped')