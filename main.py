from youtube_statistics import YTstats
from env import my_api_key

API_KEY = my_api_key
channel_uname = 'pokimane'

yt = YTstats(API_KEY, channel_uname)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()
