import os
import spotipy
import json
import time
import lyricsgenius

SPOTIFY_CLIENT_ID = 'YOURID'
SPOTIFY_CLIENT_SECRET = 'YOURSECRET'
SPOTIFY_CLIENT_URI = "https://google.com"
GENIUS_ACCESS_TOKEN = 'YOURTOKEN'

scope = 'user-read-currently-playing'

oauth_object = spotipy.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID
,client_secret=SPOTIFY_CLIENT_SECRET
,redirect_uri=SPOTIFY_CLIENT_URI
,scope=scope)


tokenDict = oauth_object.get_access_token()
token = tokenDict['access_token']



#spotify object
spotipy_object = spotipy.Spotify(auth=token)

#genius object
genius_object = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

current = spotipy_object.currently_playing()

artist_name = current['item']['album']['artists'][0]['name']
song_title = current['item']['name']



while True:
    current = spotipy_object.currently_playing()
    status = current['currently_playing_type']

    if status == 'track':
        artist_name = current['item']['album']['artists'][0]['name']
        song_title = current['item']['name']   

        length = current['item']['duration_ms']
        progress = current['progress_ms']
        time_left = int(((length-progress)/1000))     
        
        song = genius_object.search_song(title=song_title, artist= artist_name)
        lyrics = song.lyrics
        print(lyrics)
        print("\n\n\n")

        time.sleep (time_left)