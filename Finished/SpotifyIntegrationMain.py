#lines 6-60 from https://github.com/perelin/spotipy_oauth_demo/blob/master/spotipy_oauth_demo.py 

from spotifyclient import SpotifyClient
import json
import os
from bottle import route, run, request
import spotipy
from spotipy import oauth2

PORT_NUMBER = 8080
SPOTIPY_CLIENT_ID = 'b2a033b5ca8c4a20a4097c5578bf563b'
SPOTIPY_CLIENT_SECRET = '6dd5fa80708e4215a78e498cf0e70604' #bad practice i know, but i need it to work for the teachers
SPOTIPY_REDIRECT_URI = 'http://localhost:8080'
SCOPE = 'user-library-read user-read-recently-played user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-modify-public'
CACHE = '.spotipyoauthcache'
test = ""

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

def main():

    #sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

    @route('/')
    def index():
            
        access_token = ""

        token_info = sp_oauth.get_cached_token()

        if token_info:
            print("Found cached token!")
            access_token = token_info['access_token']
        else:
            url = request.url
            code = sp_oauth.parse_response_code(url)
            if code != url:
                print("Found Spotify auth code in Request URL! Trying to get valid access token...")
                try:
                    token_info = sp_oauth.get_access_token(code)
                    access_token = token_info['access_token']
                except:
                    return htmlForLoginButton

        if access_token:
            print("Access token available! Trying to get user information...")
            sp = spotipy.Spotify(access_token)
            results = sp.current_user()
            return results

        else:
            return htmlForLoginButton()

    def htmlForLoginButton():
        auth_url = getSPOauthURI()
        htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
        return htmlLoginButton

    def getSPOauthURI():
        auth_url = sp_oauth.get_authorize_url()
        return auth_url

    run(host='', port=8080)


def getSong(emotion):
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        print("no available token, errors abound")

    spotifyObj = spotipy.Spotify(token_info['access_token'])
    spClient = SpotifyClient(token_info['access_token'],SPOTIPY_CLIENT_ID)

    nbrOfTracks = 3

    lastPlayedTracks = spClient.get_last_played_tracks(nbrOfTracks)

    print(f"the {nbrOfTracks} last tracks you listened to were: ")
    for index, track in enumerate(lastPlayedTracks):
        print(f"{index+1}- {track}")

    seed = emotionCompiler(emotion)

    seedSongs = lastPlayedTracks

    recommendedTracks = spClient.get_recommended_tracks(seed, seedSongs) 
    print("here are the recomended tracks")

    for index, track in enumerate(recommendedTracks):
        print(f"{index+1}- {track}")

    start_playback(track, spotifyObj)

def emotionCompiler(emotion = 'Happy'):
    seed = [0.5 #acousticness
        ,0.5 #danceability
        ,0.5 #target_energy
        ,0.5 #instrumentalness
        ,4 #target_key ##
        ,0.5 #target_liveness
        ,0.5 #target_loudness
        ,1 #target_mode ##
        ,0.5 #target_speechiness
        ,116 #target_tempo
        ,0.5 #valence (happiness)
        ]
    if (emotion == "Happy"):
        seed = [0.5 #acousticness
            ,0.75 #danceability
            ,0.75 #target_energy
            ,0.5 #instrumentalness
            ,5 #target_key
            ,0.5 #target_liveness
            ,0.5 #target_loudness
            ,5 #target_mode (5, lydian, happy)
            ,0.5 #target_speechiness
            ,150 #target_tempo
            ,1 #valence
        ]

    if (emotion == "Sad"):
        seed = [0.5 #acousticness
            ,0.25 #danceability
            ,0.25 #target_energy
            ,0.5 #instrumentalness
            ,2 #target_key
            ,0.25 #target_liveness
            ,0.25 #target_loudness
            ,2 #target_mode (2, hypodorian, sad)
            ,0.5 #target_speechiness
            ,80 #target_tempo
            ,0 #valence
        ]

    if (emotion == "Angry"):
        seed = [0.5 #acousticness
        ,0.25 #danceability
        ,1 #target_energy
        ,0.25 #instrumentalness
        ,3 #target_key
        ,1 #target_liveness
        ,1 #target_loudness
        ,3 #target_mode (3, phrygian, angry)
        ,0.75 #target_speechiness
        ,165 #target_tempo
        ,0.1 #valence
        ]

    return seed


def start_playback(tracks, spotifyObj):
    print("startng playback")
    print(tracks)
    devices = spotifyObj.devices()
    deviceID = devices['devices'][0]['id']
    trackURIList = []
    trackURIList.append(tracks.create_spotify_uri())
    spotifyObj.start_playback(deviceID, None, trackURIList)

    return



#main()
#getSong('happy')
