from spotify_auth import get_access, get_username
import json
import requests

class Playlist:

    # Playlist constructor
    def __init__(self, setlist_data):
        self.setlist_data = setlist_data
        self.playlist_id = self.create_playlist()

    # creates a new empty spotify playlist to add songs to
    def create_playlist(self):

        artist = self.setlist_data["artist"]["name"]

        # some setlist do not have a tour name
        if "tour" in self.setlist_data:
            tour_name = self.setlist_data["tour"]["name"]
        else:
            tour_name = "Setlist"

        query = f"https://api.spotify.com/v1/users/{get_username()}/playlists"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_access()}"
        }

        # create request dict and convert to json
        request_body = json.dumps({
            "name": f"{artist} - {tour_name}",
            "description": f"Setlist Playlist for {tour_name}",
            "public": True
        })

        # send the request and save the response
        response = requests.post(query, data=request_body, headers=headers)

        # raise an exception if the status code is not successful
        response.raise_for_status()

        # grab new playlist id from response
        playlist_id = response.json()["id"]

        # console log
        playlist_name = response.json()["name"]
        print(f"playlist {playlist_name} successfully created...")

        return playlist_id

    def get_spotify_uri(self): # searches for a song

        artist = self.setlist_data["artist"]["name"]

        # create a list of all the songs
        song_list = []
        for set_data in self.setlist_data["sets"]["set"]:
            for song_data in set_data["song"]:
                song_list.append(song_data["name"])

        # retrieve the spotify uri for the song and adds it to the uri list
        uri_list = []
        for song in song_list:
            # query that searches for song and returns the full search results
            query = f"https://api.spotify.com/v1/search?query=track%3A{song}+artist%3A{artist}&type=track&offset=0&limit=20"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {get_access()}"
            }
            # send the request and save the response
            response = requests.get(query, headers=headers)

            # raise an exception if the status code is not successful
            response.raise_for_status()

            # full song search results
            songs = response.json()["tracks"]["items"]

            # sometimes the setlist song is not found and no search results are returned
            # this ensures that an index error does not occur if the search results are empty
            if len(songs) > 0:

                # only use the first song, not always the correct song / version
                uri = songs[0]["uri"]
                print(f"found {uri}...")
                uri_list.append(uri)

        return uri_list


    # add all the found setlist songs to the new playlist
    def add_song_to_playlist(self, uri_list):

        query = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_access()}"
        }

        # create request dict and convert to json
        request_body = json.dumps({
            "uris": uri_list,
        })

        # send the request and save the response
        response = requests.post(query, data=request_body, headers=headers)

        # raise an exception if the status code is not successful
        response.raise_for_status()

        print("songs successfully added :)")

        return request_body

