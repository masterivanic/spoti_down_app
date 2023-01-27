
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import requests
from spotipy.cache_handler import MemoryCacheHandler
import requests
from type import Type
from tracks import Track, TrackDto
from type import Type



class SpotifyUtils:

    @staticmethod
    def __pack_album(album) -> list:
        tracks = []
        for track in album['tracks']['items']:
            track_data = track
            track_data['album'] = album
            tracks.append(Track(track_data))

        return tracks

    @staticmethod
    def __pack_playlist(playlist, is_playlist_panel: bool = False) -> list:
        tracks = []
        for track in playlist['tracks']:
            if track is not None:
                track_data = track['track']
                if track_data is not None:
                    if is_playlist_panel:
                        tracks.append(TrackDto(track_data))
                    else:
                        track_data['playlist'] = f"{playlist['name']} - {playlist['owner']['display_name']}"
                        tracks.append(Track(track_data))
        return tracks


class SpotifyCustomer:

    SPOTIFY_CLIENT_ID = None
    SPOTIFY_CLIENT_SECRET_KEY = None
    USER_ID = None
    SPOTIPY_REDIRECT_URI = 'https://localhost:8080/'
    scopes = 'playlist-modify-public, playlist-modify-private, user-top-read, user-read-recently-played'

    def __init__(self) -> None:
        self.auth_manager = SpotifyOAuth(
            client_id=self.SPOTIFY_CLIENT_ID,
            client_secret=self.SPOTIFY_CLIENT_SECRET_KEY,
            redirect_uri=self.SPOTIPY_REDIRECT_URI,
            scope=self.scopes,
            cache_handler=None
        )
        self.sp_utils = SpotifyUtils()

        #self.auth_manager = SpotifyClientCredentials(client_id=self.SPOTIFY_CLIENT_ID,client_secret=self.SPOTIFY_CLIENT_SECRET_KEY, cache_handler=None)
        token_info = self.auth_manager.get_access_token()

        if isinstance(token_info, dict):
            self.auth_manager.cache_handler = MemoryCacheHandler(
                token_info=token_info)
            self.auth_manager.cache_handler.save_token_to_cache(
                token_info=token_info)
            self.client = spotipy.Spotify(
                auth_manager=self.auth_manager, language=None)

    def is_token_expired(self) -> bool:
        now = int(time.time())
        return self.client.auth_manager.cache_handler.get_cached_token()["expires_at"] - now < 60

    def get_user_plalists(self) -> list:
        try:
            if not self.is_token_expired():
                user_playlist = []
                playlists = self.client.user_playlists(self.USER_ID)
                while playlists:
                    for i, playlist in enumerate(playlists['items']):
                        user_playlist.append({
                            'name': playlist['name'],
                            'id': playlist['id'],
                            'uri': playlist['external_urls']['spotify']
                        })
                    if playlists['next']:
                        playlists = self.client.next(playlists)
                    else:
                        playlists = None
                return user_playlist
        except Exception:
            return []

    def get_specific_albums_tracks(self, album_id) -> any:
        if not self.is_token_expired():
            albums = self.client.album_tracks(
                album_id, limit=50, offset=0, market=None)
            return albums

    def get_artist(self, name) -> str:
        if not self.is_token_expired():
            results = self.client.search(q='artist:' + name, type='artist')
            items = results['artists']['items']
            if len(items) > 0:
                return items[0]
            return None

    def show_artist_albums(self, artist) -> None:
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

    def get_current_user(self) -> any:
        try:
            current_user = self.client.current_user()
            return current_user
        except Exception as err:
            print(err)

    def get_user(self) -> any:
        user = self.client.user(self.USER_ID)
        if user is not None:
            return user

    def get_playlist_items(self, playlist_id) -> str:
        playlist_items = self.client.playlist_items(
            playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
        return playlist_items['items']

    def search_song(self, query) -> tuple:
        song = self.client.search(query, limit=1, offset=0, type="track")
        return (
            song['tracks']['items'][0]['external_urls']['spotify'],
            song['tracks']['items'][0]['artists'][0]['name'],
            song['tracks']['items'][0]['name']
        )

    def search(self, query, query_type=Type.TRACK) -> list:
        results = self.client.search(q=query, limit=1, type=query_type)
        if len(results[query_type + 's']['items']) > 0:
            if query_type == Type.TRACK:
                return [Track(results[Type.TRACK + 's']['items'][0])]
            elif query_type == Type.ALBUM:
                return self.sp_utils._SpotifyUtils__pack_album(self.client.album(results[Type.ALBUM + 's']['items'][0]['id']))
            elif query_type == Type.PLAYLIST:
                return self._get_playlist_tracks(results[Type.PLAYLIST + 's']['items'][0]['id'])
        else:
            return []

    def link(self, query) -> list:
        try:
            if '/track/' in query:
                return [Track(self.client.track(query))]
            elif '/album/' in query:
                return self.sp_utils._SpotifyUtils__pack_album(self.client.album(query))
            elif '/playlist/' in query:
                return self._get_playlist_tracks(query)
            else:
                return []
        except Exception:
            return []

    def _get_playlist_tracks(self, playlist_id, is_playlist_panel: bool = False) -> list:
        playlist = self.client.playlist(playlist_id)
        results = playlist['tracks']
        tracks = results['items']
        while results['next']:
            results = self.client.next(results)
            tracks.extend(results['items'])

        playlist['tracks'] = tracks
        return self.sp_utils._SpotifyUtils__pack_playlist(playlist, is_playlist_panel)

    def _get_playlist_name(self, playlist_id) -> str:
        return self.client.playlist(playlist_id)['name']

    def create_playlists(self, playlist_name: str) -> bool:
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
                public=True
            )
        return is_created

    def is_playlist_exist(self, playlist_name: str) -> tuple:
        all_playlist = self.get_user_plalists()
        track, exist = None, False
        for track in all_playlist:
            if track['name'] == playlist_name:
                track, exist = track, True
                break
        return track, exist

    def is_song_exist(self, playlist_title: str, song_uri: str) -> bool:
        track, exist = self.is_playlist_exist(playlist_title)
        is_uri = False
        if track['name'] == playlist_title:
            items = self.client.playlist(
                playlist_id=track['id'], additional_types=('track', ))
            for song in items['tracks']['items']:
                if song_uri == song['track']['external_urls']['spotify']:
                    is_uri = True
                    break
        return is_uri

    async def add_items_in_playlist(self, playlist_name: str, tracks: list) -> None:
        if not self.is_token_expired():
            track, is_exist = self.is_playlist_exist(playlist_name)
            if is_exist:
                self.client.playlist_add_items(track['id'], tracks)

    def delete_playlist(self, playlist_id: str) -> None:
        self.client.user_playlist_unfollow(
            user=self.client.current_user()['id'],
            playlist_id=playlist_id
        )
      

if __name__ == '__main__':
    pass

   