# SetlistToPlaylist
A python script that takes a Setlist.fm url, and generates a Spotify playlist with the songs from the setlist.

## Table of Contents
* [Technologies](#Technologies)
* [Setup](#LocalSetup)
* [ToDo](#ToDo)
* [Troubleshooting](#Troubleshooting)

## Technologies
* Setlist.fm API
* Spotify Web API
* Flask
* Requests Library


## LocalSetup
1) Install all dependencies   
`pip3 install -r requirements.txt`

2) Request an API key from Setlist.fm and save to setlist_auth.py file

3) Create a Spotify app - instructions for this in Spotify API documentation

4) The spotify api calls require oauth 2.0. Make changes to spotify_auth.py create_spotify_oauth function.

5) Run the File  
`python3 main.py`   
    * you will be asked for the Setlist.fm url
    * you will then be prompted to login and authorize the Spotify app.


## ToDo
* Tests

## TroubleShooting
* yo, lots of things will break... be careful 
