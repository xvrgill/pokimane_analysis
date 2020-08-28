from pokimane_comments import YTcomments

API_KEY = 'AIzaSyCuz9GIL72hTM-MtPfqWPWfyaDCmarcSsM'

yt = YTcomments(API_KEY)
yt.get_all_comments()
yt.dump()
