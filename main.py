from youtube_statistics import YTstats

API_KEY = 'AIzaSyAp9Y-hUx6ToKlf7GJH0C_1Dm3ocqJL2X4'
channel_uname = 'pokimane'
channel_id = 'UChXKjLEzAB1K7EZQey7Fm1Q'

# Creates json file with channel info from channel username
# yt = YTstats(API_KEY, channel_uname)
# yt.get_channel_statistics()
# yt.dump()

yt = YTstats(API_KEY, channel_id)
yt.get_channel_video_data()