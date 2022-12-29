
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from datetime import date
import logging
import json
import requests
from spotipy.cache_handler import MemoryCacheHandler


class SpotifyCustomer:

    SPOTIFY_CLIENT_ID = None
    SPOTIFY_CLIENT_SECRET_KEY = None
    USER_ID = None
    SPOTIPY_REDIRECT_URI = 'http://localhost:8080/'
    scopes = 'playlist-modify-public, user-top-read, user-read-recently-played'

    def __init__(self) -> None:

        self.auth_manager = SpotifyOAuth(
            client_id=self.SPOTIFY_CLIENT_ID,
            client_secret=self.SPOTIFY_CLIENT_SECRET_KEY,
            redirect_uri=self.SPOTIPY_REDIRECT_URI,
            scope=self.scopes,
            cache_handler=None
        )
        #self.auth_manager = SpotifyClientCredentials(client_id=self.SPOTIFY_CLIENT_ID,client_secret=self.SPOTIFY_CLIENT_SECRET_KEY, cache_handler=None)
        token_info = self.auth_manager.get_access_token()

        if isinstance(token_info, dict):
            self.auth_manager.cache_handler = MemoryCacheHandler(
                token_info=token_info)
            self.auth_manager.cache_handler.save_token_to_cache(
                token_info=token_info)
            self.client = spotipy.Spotify(
                auth_manager=self.auth_manager, language=None)

    def is_token_expired(self):
        now = int(time.time())
        return self.client.auth_manager.cache_handler.get_cached_token()["expires_at"] - now < 60

    def get_user_plalists(self):
        if not self.is_token_expired():
            user_playlist = []
            playlists = self.client.user_playlists(self.USER_ID)
            while playlists:
                for i, playlist in enumerate(playlists['items']):
                    print("%4d %s %s %s" % (
                        i + 1 + playlists['offset'], playlist['uri'],  playlist['name'], playlist['id']))
                    user_playlist.append({
                        'name': playlist['name'],
                        'id': playlist['id']
                    })
                if playlists['next']:
                    playlists = self.client.next(playlists)
                else:
                    playlists = None
            return user_playlist

    def get_specific_albums_tracks(self, album_id):
        if not self.is_token_expired():
            albums = self.client.album_tracks(
                album_id, limit=50, offset=0, market=None)
            return albums

    def get_artist(self, name):
        if not self.is_token_expired():
            results = self.client.search(q='artist:' + name, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                return items[0]
            else:
                return None

    def show_artist_albums(self, artist):
        if not self.is_token_expired():
            albums = []
            results = self.client.artist_albums(
                artist['id'], album_type='album')
            albums.extend(results['items'])
            while results['next']:
                results = self.client.next(results)
                albums.extend(results['items'])
            seen = set()
            albums.sort(key=lambda album: album['name'].lower())

            for album in albums:
                name = album['name']
                if name not in seen:
                    seen.add(name)

    def get_current_user(self):
        try:
            current_user = self.client.current_user()
            return current_user
        except Exception as err:
            print(err)

    def get_user(self):
        user = self.client.user(self.USER_ID)
        if user is not None:
            return user

    def get_playlist_items(self, playlist_id):
        playlist_items = self.client.playlist_items(
            playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
        return playlist_items['items']

    def search_song(self, query):
        song = self.client.search(query, limit=1, offset=0, type="track")
        return (
            song['tracks']['items'][0]['external_urls']['spotify'],
            song['tracks']['items'][0]['artists'][0]['name'],
            song['tracks']['items'][0]['name']
        )

    def create_playlists(self, playlist_name: str):
        all_playlist = self.get_user_plalists()
        is_created = False
        for track in all_playlist:
            if track['name'] == playlist_name:
                is_created = True
                break

        if not is_created:
            self.client.user_playlist_create(
                self.USER_ID,
                playlist_name,
                public=False
            )
        return is_created

    def is_playlist_exist(self, playlist_name: str):
        all_playlist = self.get_user_plalists()
        track, exist = None, False
        for track in all_playlist:
            if track['name'] == playlist_name:
                track, exist = track, True
                break
        return track, exist

    def add_items_in_playlist(self, playlist_name: str, tracks: list):
        if not self.is_token_expired():
            track, is_exist = self.is_playlist_exist(playlist_name)
            if is_exist:
                self.client.playlist_add_items(track['id'], tracks)


if __name__ == '__main__':
    SpotifyCustomer().get_user_plalists()
    # print(SpotifyCustomer().get_user())
    # print(SpotifyCustomer().get_current_user())
    # print(SpotifyCustomer().get_playlist_items('0eLIikVh2b8Wg1ucYceFl'))
    # SpotifyCustomer().create_playlists('MyPlaylist1')
    # SpotifyCustomer().add_items_in_playlist('Beest', [
    #     'https://open.spotify.com/track/27qAMKrDdKEs8HDXcvR24R?si=fd135908b26f40a0'])
