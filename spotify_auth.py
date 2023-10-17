from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect
import time


ACCESS_TOKEN = ''  # TODO: update

# initialize flask app, set session cookie, set a random secret key to sign the cookie
app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'spotify cookie'
app.secret_key = '' # TODO: update

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

    # will return authentication status. server must be shut down at this point to continue execution
    if not token:
        return 'authentication failed!'
    else:
        return 'access token retrieved. authentication successful!'


def create_spotify_oauth():
    # client id and secret are found on the created spotify app
    return SpotifyOAuth(
        client_id='',
        client_secret='',
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private'
    )  # TODO: update

# spotify client secret information
# function for token handling - retrieves, refreshes and saves the access token
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

    # full token info can be found in .cache, only want the access token
    access_token = token_info['access_token']

    # saves the cached access token to the global variable below
    global ACCESS_TOKEN
    ACCESS_TOKEN = access_token

    return access_token


# this gets called after the server is shut down, simply importing global variable instead returns empty string
def get_access():
    return ACCESS_TOKEN


# hard coded username...
def get_username():  # TODO: update
    return None