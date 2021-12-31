import os
import spotipy
import json
import time
import lyricsgenius

SPOTIFY_CLIENT_ID = '644c1c2f06004cb38def04c9642bb301'
SPOTIFY_CLIENT_SECRET = 'c84452d7019c4aad9003149adcc57cb9'
SPOTIFY_CLIENT_URI = "https://google.com"
GENIUS_ACCESS_TOKEN = 'yAeBehh7VL7uXMvgEOrzEsoKZtJAetMFetFRm9pdpDNoVBVyxrzLPlbHAfjADQJw'

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

#strips the word of any punctuation
def strip_word(word):
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    new_word = word
    for l in word:
        if l in punctuation:
            new_word = new_word.replace(l,"")
    return new_word

tot_words = set()
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
        #for checking how many words the user has listened to since they started
        words = lyrics.split()
        for word in words:
            temp = strip_word(word)
            tot_words.add(temp)
           
        print(lyrics)
        print("\n\n\n")
        print("So Far, You Have Listened to " + str(len(tot_words)) + " unique words!")
        

        time.sleep (time_left)

