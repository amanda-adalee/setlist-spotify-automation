from setlist import Setlist
from playlist import Playlist
import spotify_auth


if __name__ == '__main__':
    ''' setlist.fm '''
    #url = input("Enter the setlist url:")
    url = "https://www.setlist.fm/setlist/the-wonder-years/2023/rams-head-live-baltimore-md-3a23933.html"
    setlist = Setlist(url)

    ''' spotify '''
    spotify_auth.app.run(debug=False)
    playlist = Playlist(setlist.json_data)
    uris = playlist.get_spotify_uri()
    playlist.add_song_to_playlist(uris)


