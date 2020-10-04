from pokimane_comments import YTcomments
from env import my_api_key

API_KEY = my_api_key

yt = YTcomments(API_KEY)
yt.get_all_comments()
yt.dump()
