from setlist import Setlist
from playlist import Playlist
import spotify_auth

# project starts here
if __name__ == '__main__':
    ''' setlist.fm '''
    url = input("Enter the setlist url:")
    setlist = Setlist(url)

    ''' spotify '''
    spotify_auth.app.run(debug=False)  # TODO: programmatically shut down server to continue execution
    playlist = Playlist(setlist.json_data)
    uris = playlist.get_spotify_uri()
    playlist.add_song_to_playlist(uris)