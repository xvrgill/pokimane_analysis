from pokimane_comments import PokimaneComments

API_KEY = 'AIzaSyANjsTff1LbA7-MuhnJhbu88-LlDE9wjL4'
channel_uname = 'pokimane'

pc = PokimaneComments(API_KEY, channel_uname)
pc.get_channel_statistics()
pc.get_channel_video_data()
pc.dump()