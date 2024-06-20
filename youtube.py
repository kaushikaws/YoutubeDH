
from googleapiclient.discovery import build
import pymongo
import pandas as pd
import streamlit as st
#API key connection
 
def Api_connect():
    Api_Id = "AIzaSyBXy02RuPxzfbnML_UdH5vSL_UBLMILpJ0"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = build(api_service_name,api_version,developerKey=Api_Id)
    return youtube
youtube = Api_connect()

#get channels information

def get_channel_info(channel_id):
    request=youtube.channels().list(
                                part="snippet,ContentDetails,statistics",
                                                    id=channel_id
                                                        )
    response = request.execute()
    for i in response['items']:
        data = dict(Channel_Name = i["snippet"]["title"],
                    Channel_Id=i["id"],Subscribers=i['statistics']['subscriberCount'],
                    Views=i["statistics"]["viewCount"],
                    Total_Videos=i["statistics"]["videoCount"],
                    Channel_Description=i["snippet"]["description"],
                    Playlist_Id=i["contentDetails"]["relatedPlaylists"]["uploads"])
        return data
channel_details = get_channel_info("UCX6OQ3DkcsbYNE6H8uQQuVA")

#get video ids

def get_videos_ids(channel_id):
    video_ids=[]
    response=youtube.channels().list(id=channel_id,part = 'contentDetails').execute()
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None
    while True:
         response1=youtube.playlistItems().list(part='snippet',playlistId=Playlist_Id,maxResults=50,
                                                pageToken=next_page_token).execute()
         for i in range(len(response1['items'])):
             video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
         next_page_token=response1.get('nextPageToken')
         if next_page_token is None:
             break
    return video_ids
video_details = get_videos_ids("UCQ8kBZG9KpEEB7nFSNOS62A")

#get video info


