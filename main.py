from youtube_statistics import YTstats

# TODO: Make it so that only uname is required. Channel id should be retrieved from api.
# TODO: Allow for user input to turn into a repeatable script that can be shared with the community.
# channel_uname = 'pokimane'

API_KEY = 'AIzaSyAp9Y-hUx6ToKlf7GJH0C_1Dm3ocqJL2X4'
channel_id = 'UChXKjLEzAB1K7EZQey7Fm1Q'

# Creates json file with channel info from channel username
# yt = YTstats(API_KEY, channel_uname)
# yt.get_channel_statistics()
# yt.dump()

yt = YTstats(API_KEY, channel_id)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()
