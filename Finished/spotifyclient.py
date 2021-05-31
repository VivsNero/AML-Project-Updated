#a modified version of https://www.youtube.com/watch?v=3vvvjdmBoyc&ab_channel=ValerioVelardo-TheSoundofAI

import json
import requests
from track import Track
from playlist import Playlist


class SpotifyClient:
    def __init__(self, auth_token, user_id):
        """
        :param auth_token (str): spotify API token
        :param user_id (int): spotify user id
        """
        self.auth_token = auth_token
        self.user_id = user_id

    def api_request(self, url, data = None):
        if data is not None:
            response = requests.post(
                 url,
                 data = data,
                 headers={
                     "Content-Type": "application/json",
                     "Authorization": f"Bearer {self.auth_token}"
                 }
             )
        else:
             response = requests.get(url, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            })
        return response
    
    def create_playlist(self, name):
        data = json.dumps({
            "name":name,
            "description":"test",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self.api_request(url, data)
        response_json = response.json()
        playlist_id = response_json["id"]
        playlist = Playlist(name, playlist_id)
        return playlist

    def populate_playlist(self, playlist, tracks):
        track_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(track_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self.api_request(url, data)
        response_json = response.json()
        return response_json

    def get_last_played_tracks(self, nbrOfTracks):
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={nbrOfTracks}"
        response = self.api_request(url)
        response_json = response.json()
        tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]) for 
            track in response_json["items"]]
        return tracks

    def get_recommended_tracks(self, seed, track, limit = 1):
        """
        :param seed (list of 1 numbers): most of which are numbers between 1 and 0, with the exception of 
         target_tempo (bpm)
            * acousticness
            * danceability
            * target_energy
            * instrumentalness
            * target_key
            * target_liveness
            * target_loudness
            * target_mode
            * target_speechiness
            * target_tempo
            * valence

        :param limit (int): the number of recommended tracks
        :param tracks (track): a track to liken the song to 
        """
        url = f'''https://api.spotify.com/v1/recommendations?limit={limit}&seed_tracks={track[0].id}&
        target_acousticness={seed[0]}&target_danceability={seed[1]}&target_energy={seed[2]}&
        target_instrumentalness={seed[3]}&target_key={seed[4]}&target_liveness={seed[5]}&target_loudness={seed[6]}&
        target_mode={seed[7]}&target_speechiness={seed[8]}&target_tempo={seed[9]}&
        &target_valence={seed[10]}'''

        response = self.api_request(url)
        response_json = response.json()
        #print(response_json)
        tracks = [Track(track["name"], track["id"], track["artists"][0]["name"]) for
                    track in response_json["tracks"]]
        return tracks
    