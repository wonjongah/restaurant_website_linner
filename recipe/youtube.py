from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyDKH4KaYVdOJjN5HTg-PxFlGBEWekU3pVc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q='haha ha',
        order="date",
        part="snippet",
        maxResults=30
    ).execute()

    print(search_response)
    videos = []
    channels = []
    playlists = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                       search_result["id"]['videoId']))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                         search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                          search_result["id"]["playlistId"]))

    print("\n\nVideos:\n\n", "\n".join(videos), "\n")
    print("\n\nChannels:\n\n", "\n".join(channels), "\n")
    print("\n\nPlaylists:\n\n", "\n".join(playlists), "\n")


if __name__ == "__main__":
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=25)
    args = argparser.parse_args()

try:
    youtube_search()
except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))



# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from oauth2client.tools import argparser
#
# DEVELOPER_KEY = "AIzaSyDKH4KaYVdOJjN5HTg-PxFlGBEWekU3pVc"
# YOUTUBE_API_SERVICE_NAME="youtube"
# YOUTUBE_API_VERSION="v3"
# youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
#
#
#
# search_response = youtube.search().list(
#     q = "haha ha",
#     order = "date",
#     part = "snippet",
#     maxResults = 30
#     ).execute()
#
# for i in search_response['items']:
#     print(i.values())
#     print('####################')


#from pytchat import LiveChat
# import pafy
# import pandas as pd
#
# pafy.set_api_key('AIzaSyDKH4KaYVdOJjN5HTg-PxFlGBEWekU3pVc')
#
# video_id = 'HkT0N5QXXiM'
#
#
# v = pafy.new(video_id)
# title = v.title
# author = v.author
# published = v.published
#
# print(title)
# print(author)
# print(published)
#
#
# empty_frame = pd.DataFrame(columns=['제목', '채널 명', '스트리밍 시작 시간', '댓글 작성자', '댓글 내용', '댓글 작성 시간'])
# empty_frame.to_csv('./youtube.csv')
#
#
# chat = LiveChat(video_id = video_id, topchat_only = 'FALSE')
#
# while chat.is_alive():
#     try:
#         data = chat.get()
#         items = data.items
#         for c in items:
#             print(f"{c.datetime} [{c.author.name}]- {c.message}")
#             data.tick()
#             data2 = {'제목' : [title], '채널 명' : [author], '스트리밍 시작 시간' : [published], '댓글 작성자' : [c.author.name], '댓글 내용' : [c.datetime], '댓글 작성 시간' : [c.message]}
#             result = pd.DataFrame(data2)
#             result.to_csv('./youtube.csv', mode='a', header=False)
#     except KeyboardInterrupt:
#         chat.terminate()
#         break