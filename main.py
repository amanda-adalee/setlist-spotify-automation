from setlist import Setlist
from playlist import Playlist
import spotify_auth
import sys


# project starts here
if __name__ == '__main__':
    ''' setlist.fm '''
    url = input("Enter the setlist url:")
    #url = sys.argv[1]
    setlist = Setlist(url)

    ''' spotify '''
    spotify_auth.app.run(port=5001, debug=False)
    playlist = Playlist(setlist.json_data)
    uris = playlist.get_spotify_uri()
    playlist.add_song_to_playlist(uris)
