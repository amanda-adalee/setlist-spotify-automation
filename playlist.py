from spotify_auth import get_access, get_username
import json
import requests

class Playlist:

    def __init__(self, setlist_data):
        self.setlist_data = setlist_data
        self.playlist_id = self.create_playlist()

    # creates a new empty spotify playlist to add songs to
    def create_playlist(self):

        tour_name = self.setlist_data["tour"]["name"]
        print(tour_name)

        print(get_access())

        query = f"https://api.spotify.com/v1/users/{get_username()}/playlists"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_access()}"
        }

        # create request dict and convert to json
        request_body = json.dumps({
            "name": f"{tour_name}",
            "description": f"Setlist Playlist for {tour_name}",
            "public": True
        })
        print(request_body)
        print(headers)
        # send the request and save the response
        response = requests.post(query, data=request_body, headers=headers)

        # raise an exception if the status code is not successful
        response.raise_for_status()

        # new playlist id
        playlist_id = response.json()["id"]

        return playlist_id


    def get_spotify_uri(self): # searches for a song

        artist = self.setlist_data["artist"]["name"]

        song_list = []

        for set_data in self.setlist_data["sets"]["set"]:
            for song_data in set_data["song"]:
                song_list.append(song_data["name"])

        uri_list = []

        for song in song_list:

            query = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=20"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access()}"
            }

            response = requests.get(query, headers=headers)
            response.raise_for_status()

            response_json = response.json()
            songs = response_json["tracks"]["items"]


            # only use the first song
            uri = songs[0]["uri"]
            uri_list.append(uri)


        return uri_list


    # add all the setlist songs to the new playlist
    def add_song_to_playlist(self, uri_list):

        # create request dict and convert to json
        request_body = json.dumps({
            "uris": uri_list,
        })

        query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_access()}"
        }

        response = requests.post(query, data=request_body, headers=headers)
        response.raise_for_status()

        return request_body

