import setlist as sl
import spotify as sp

if __name__ == '__main__':
    ''' setlist.fm '''
    #user_setlist_id = input('Enter the setlist id:')
    setlist_id = "3a23933"
    setlist = sl.Setlist(setlist_id)

    ''' spotify '''
    playlist = sp.Spotify()
    playlist.get_spotify_uri(setlist.all_details)