from exceptions import ResponseException
from spotify_secrets import spotify_token, spotify_user_id

import json
import requests
import pandas

class Playlist:

    def __init__(self, setlist_data):
        self.setlist_data = self.parse_data(setlist_data)
        self.playlist_id = self.create_playlist()
        #self.uri_list = self.get_spotify_uri()

    def parse_data(self, setlist_data):

        tour_name = setlist_data["tour"]["name"]
        print(tour_name)
        artist = setlist_data["artist"]["name"]
        print(artist)
        song_list = setlist_data["sets"]["set"]

        return tour_name


    def create_playlist(self):  # creates a new empty spotify playlist to add songs to

        request_body = json.dumps({
            "name": "Testy Test",
            "description": "this is a test. i hope it works",
            "public": True
        })

        query = f"https://api.spotify.com/v1/users/{spotify_user_id}/playlists"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }

        response = requests.post(query, data=request_body, headers=headers)

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        response_json = response.json()

        print(response_json["id"])

        # new playlist id
        return response_json["id"]


    def get_spotify_uri(self, setlist_data): # searches for a song


        uri_list = []
        # todo: parse setlist data and get song name and artist
        for item in setlist_data:
            song_name = item[""][""]
            artist = item[""][""]

            query = f"https://api.spotify.com/v1/search?query=track%3A{song_name}+artist%3A{artist}&type=track&offset=0&limit=20"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {spotify_token}"
            }

            response = requests.get(query, headers=headers)

            response_json = response.json()
            songs = response_json["tracks"]["items"]

            # only use the first song
            uri = songs[0]["uri"]
            uri_list.append(uri)

        return uri_list

    def add_songs_to_playlist(self): # add all the setlist songs to the new playlist

        # new playlist id
        playlist_id = self.playlist_id

        # list of all uris
        uris = self.uri_list

        # add all songs into new playlist
        request_data = json.dumps(uris)

        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {spotify_token}"
        }

        response = requests.post(query, data=request_data, headers=headers)

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        return response.json()

    #get_spotify_uri()
    #add_songs_to_playlist()