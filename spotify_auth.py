from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import time
import spotipy

ACCESS_TOKEN = ''

# initialize flask app, set session cookie, set a random secret key to sign the cookie
app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'spotify cookie'
app.secret_key = '2eGZgynWYAPFa5'

# set the key for the token info in the session dictionary
TOKEN_INFO = ''

# route to handle user logging in to spotify
# the login function will be called when address to the app route is reached
@app.route('/')
def login():
    # create a SpotifyOAuth instance and get the authorization URL
    auth_url = create_spotify_oauth().get_authorize_url()
    # redirect the user to the authorization URL
    return redirect(auth_url)


# route to handle the redirect uri after authorization
@app.route('/redirect')
def redirect_page():

    session.clear()
    # extract/get the authorization code from the request parameters
    code = request.args.get('code')
    # exchange the authorization code for an access token and refresh token
    token_info = create_spotify_oauth().get_access_token(code)
    # save the token info in the session
    session[TOKEN_INFO] = token_info
    # redirect the user to the save_discover_weekly route
    return redirect(url_for('success_page', _external=True))


@app.route('/success')
def success_page():
    token = get_token()

    if not token:
        return 'authentication failed!'

    return 'access token retrieved. authentication successful!'


def create_spotify_oauth():

    return SpotifyOAuth(
        client_id='d361fa3114b14fbf9475300951a3bfcb',
        client_secret='5e6392016eb24f6e90573f3ea72d27bf',
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )

# spotify client_secret information
def get_token():

    token_info = session.get(TOKEN_INFO)
    # check if token info is empty, and redirect the user to login to create token info
    if not token_info:
        redirect(url_for('login', _external=False))

    # check if the token is expired or expires in less than 1 minute, and get the refresh token
    current_time = int(time.time())
    is_expired = token_info['expires_at'] - current_time < 60
    if is_expired:
        token_info = create_spotify_oauth().refresh_access_token(token_info['refresh_token'])

    access_token = token_info['access_token']

    global ACCESS_TOKEN
    ACCESS_TOKEN = access_token

    return access_token

def get_access():
    return ACCESS_TOKEN
# hard coded username
def get_username():
    return "vjiijnceu24pbs6p3i1g77efa"