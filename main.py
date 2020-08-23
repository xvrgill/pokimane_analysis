from youtube_statistics import YTstats

API_KEY = 'AIzaSyANjsTff1LbA7-MuhnJhbu88-LlDE9wjL4'
channel_uname = 'pokimane'

yt = YTstats(API_KEY, channel_uname)
yt.get_channel_statistics()
yt.get_channel_video_data()
yt.dump()
