from setlist import Setlist
from playlist import Playlist

from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import time
import spotipy

# initialize Flask app
app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = 'spotify cookie'

# set a random secret key to sign the cookie
app.secret_key = '2eGZgynWYAPFa5'

# set the key for the token info in the session dictionary
TOKEN_INFO = 'token_info'


# route to handle logging in
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)


# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    session.clear()
    # get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('save_discover_weekly', _external=True))


# route to save the Discover Weekly
@app.route('/saveDiscoverWeekly')
def save_discover_weekly():
    try:
        # get the token info from the session
        token_info = get_token()
    except:
        # if the token info is not found, redirect the user to the login route
        print('User not logged in')
        return redirect("/")

    return ('OATH Successful')


# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login', _external=False))

    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id='d361fa3114b14fbf9475300951a3bfcb',
        client_secret='5e6392016eb24f6e90573f3ea72d27bf',
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

def get_setlist_id():
    #url = input("Enter the setlist url:")
    url = "https://www.setlist.fm/setlist/the-wonder-years/2023/rams-head-live-baltimore-md-3a23933.html"
    last_dash_index = url.rfind("-")
    last_period_index = url.rfind(".")
    setlist_id = url[last_dash_index+1:last_period_index]

    return setlist_id


if __name__ == '__main__':
    ''' setlist.fm '''
    setlist = Setlist(get_setlist_id())

    ''' spotify '''
    #app.run(debug=True)
    playlist = Playlist(setlist.json_data)