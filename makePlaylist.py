import httplib2
import os
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.developers.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
  message=MISSING_CLIENT_SECRETS_MESSAGE,
  scope=YOUTUBE_READ_WRITE_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
  flags = argparser.parse_args()
  credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
  http=credentials.authorize(httplib2.Http()))

channelId = "UCTQpv70KPMZ-YWGuWBC-TqA"
playlistId = "PLikXBwz5Lef7BpLZAZHEgmyLBMagxW5Xa"

nextPageToken = None
channelVideos = []

print("get channel's videos")
while True:
  video_list_response = youtube.search().list(
    part="id, snippet",
    channelId=channelId,
    order="date",
    maxResults=50,
    pageToken=nextPageToken
  ).execute()

  for item in video_list_response["items"]:
    if item["id"]["kind"] == "youtube#video" and not "#shorts" in item["snippet"]["title"]:
      channelVideos.append(item["id"]["videoId"])

  nextPageToken = video_list_response.get("nextPageToken")
  if nextPageToken == None:
    break;

print("get playlist's videos")
playlistVideos = []
nextPageToken = None

while True:
    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlistId,
        pageToken=nextPageToken
    )
    response = request.execute()

    for item in response['items']:
        playlistVideos.append(item['snippet']['resourceId']['videoId'])

    nextPageToken = response.get('nextPageToken')

    if nextPageToken is None:
        break

print("add video to playlist")
new_videos = list(set(channelVideos) - set(playlistVideos))
new_videos.reverse()

for video_id in new_videos:
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
          "snippet": {
            "playlistId": playlistId,
            "position": 0,
            "resourceId": {
              "kind": "youtube#video",
              "videoId": video_id
            }
          }
        }
    )
    response = request.execute()

print("New videos added to the playlist!")
