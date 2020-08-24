import requests
import json
from tqdm import tqdm

# Set global variables
API_KEY = 'AIzaSyAp9Y-hUx6ToKlf7GJH0C_1Dm3ocqJL2X4'

# Import video ids

# Open the json file with all data as python dictionary
with open('pokimane.json', 'r') as f:
    p_video_data = json.load(f)
# Get the channel id with .keys() - returns dict_keys([]) object   
channel_id_dict = p_video_data.keys()
# Get channel id out of dict with list - turns it into a list so that we can call its index
channel_id = list(p_video_data)[0]
# Retrieve data by storing the value associated with the first key in our json which is the channel id
data = p_video_data.get(channel_id)

# Retrieve video data

# Get video data from imported json with .get()
video_data = data.get('video_data')
# Create a new empty dictionary to store our newly formatted data
comment_data = dict()


# Get comment data
def _get_comment_data(api_key, video_id):
    url = f'https://www.googleapis.com/youtube/v3/commentThreads?key={api_key}&videoId={video_id}&part=snippet&part=replies&maxResults=100'
    com, npt = _get_comment_data_per_page(url, video_id)
    while(npt is not None):
        next_url = url + '&pageToken=' + npt
        next_comment, npt = _get_comment_data_per_page(next_url, video_id)
        com.update(next_comment)
    return com


def _get_comment_data_per_page(url, video_id):
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    npt = data.get('nextPageToken', None)
    # Got an error because you can't call an index on none
    # Wrap in try statement to set comments to none if the 'items' object is not in the response
    try:
        comments = data.get('items')[0]
    except:
        # Tell the user when an error occurs in the above function.
        # Script must continue and none can't be returned with the above code.
        # When above function cant be run, no comments exist for video.
        # When no comments are available, it means the comments are turned off.
        # Instead, set comments to none below.
        print(f'Video {video_id} has comments turned off. Returning none for item.')
        comments = None
    return comments, npt

# Loop through our video data to get the id of each video as a key and an empty dictionary as the value
print('creating dictionary of video ids')
for thing in tqdm(video_data):
    comment_data.update({thing : dict()})
print('retrieving and adding comment data to video ids')
for item in tqdm(video_data):
    retrieved_comments = _get_comment_data(API_KEY, item)
    try:
        comment_data[item].update(retrieved_comments)
    except:
        print('error updating retrieved comments')
    
# Dump our newly formatted json data into a json file named video_comments.json
with open('video_comments.json', 'w') as f:
    json.dump(comment_data, f, indent=4)