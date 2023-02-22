import re
import pandas as pd
from typing import List
from enum import Enum
from numpy import dtype
from pathlib import Path
from collections import Counter
from unidecode import unidecode
from spotipy import Spotify as SpotifyApi
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius as GeniusApi


with open('pt_stopwords.txt', 'r', encoding='utf-8') as file:
    PORTUGUESE_STOP_WORDS = list(map(unidecode, file.read().splitlines()))
    file.close()

with open('en_stopwords.txt', 'r', encoding='utf-8') as file:
    ENGLISH_STOP_WORDS = list(map(unidecode, file.read().splitlines()))
    file.close()

ALL_STOP_WORDS = PORTUGUESE_STOP_WORDS.copy()
ALL_STOP_WORDS.extend(ENGLISH_STOP_WORDS)


GENIUS_CLIENT_ID = '9qC_Mp3ny7eUj-tzz0emyMabaytb2kXFt8Sk1jplAMSgDd0DE9Lq0E-Y_BHxZm5x'
GENIUS_CLIENT_SECRET = '-q_QcO7hZQnjXbOEK0dpyBvtbUH5uGxmLediIdPfk_eVzsFtDh_2mr8wrp41wPNwtPjWg0N9Rw37e8KmEFeU8A'
GENIUS_ACCESS_TOKEN = 'qtZInoL-MhAzuGzSQRi9_K8oX-D5lh7LqU9VhZpNWTqoReWFhADj_4Ewy5wmBU2z'
SPOTIFY_CLIENT_ID = '43ab55a3bafb463297b4ed113b7b9b23'
SPOTIFY_CLIENT_SECRET = '75a730701292478bb95c056c1c8c02b5'
SPOTIFY_REDIRECT_URI = 'http://localhost/'


class Language(Enum):
    """Relação de palavras que devem ser ignoradas em cada idioma."""
    PT = PORTUGUESE_STOP_WORDS
    EN = ENGLISH_STOP_WORDS
    ALL = ALL_STOP_WORDS


class Genius(GeniusApi):
    def __init__(self, access_token=GENIUS_ACCESS_TOKEN):
        self.client_id = GENIUS_CLIENT_ID
        self.client_secret = GENIUS_CLIENT_SECRET
        self.access_token = access_token
        super().__init__(self.access_token)

    def get_song_lyrics(self, song: str, artist: str) -> List[str]:
        """Buscar letra de uma determinada música."""
        try:
            song_lyrics = self.search_song(song, artist).lyrics
        except AttributeError:
            return []
        song_lyrics = re.sub(r'\[(.*?)\]', '', song_lyrics)
        song_lyrics = song_lyrics.replace('"', '').replace('“', '').replace('”', '')
        song_lyrics = song_lyrics.replace('.', ' ').replace(',', ' ').replace(';', ' ')
        song_lyrics = song_lyrics.replace('EmbedShare', '')
        song_lyrics = song_lyrics.replace('URLCopyEmbedCopy', '')
        song_lyrics = song_lyrics.replace('\n', ' ')
        song_lyrics = song_lyrics.replace('(', '').replace(')', '').replace('{', '').replace('}', '')
        song_lyrics = song_lyrics.lower()
        song_lyrics = unidecode(song_lyrics)
        # Normalize
        return song_lyrics.split()


class Spotify:
    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.redirect_uri = SPOTIFY_REDIRECT_URI
        self.scope = 'user-library-read'
        self.api = self.authorize()
        self.genius_api = Genius()

    def authorize(self):
        """Fazer a autorização na API."""

        auth = dict(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=self.scope)
        return SpotifyApi(auth_manager=SpotifyOAuth(**auth))

    def get_playlist_content(self, playlist_id: str) -> pd.DataFrame:
        """Buscar relação de músicas e artistas em uma determinada playlist."""

        raw_data = self.api.playlist(playlist_id)
        playlist_name = f'''"{raw_data['name']}" by {raw_data['owner']['display_name']}'''
        tracks = raw_data['tracks']['items']
        playlist_df = pd.DataFrame(dict(Song=[], Artist=[]), dtype=dtype(str))
        for index, track in enumerate(tracks):
            track_name = track['track']['name']
            track_artists = '; '.join([artist['name'] for artist in track['track']['album']['artists']])
            playlist_df.at[index, 'Song'] = track_name
            playlist_df.at[index, 'Artist'] = track_artists
        return playlist_df

    def get_playlist_words(self, playlist_data: pd.DataFrame, lang: Language = Language.ALL, top: int = 20) -> pd.DataFrame:
        """Buscar as palavras mais usadas em uma determinada playlist."""

        if 'Song' in playlist_data.columns and 'Artist' in playlist_data.columns:
            all_songs_lyrics = []
            for row in playlist_data.itertuples():
                artist_name = row.Artist.split('; ')[0]
                song_name = row.Song
                song_lyrics = self.genius_api.get_song_lyrics(song=song_name, artist=artist_name)
                song_lyrics = list(filter(lambda x: x not in lang.value, song_lyrics))
                all_songs_lyrics.extend(song_lyrics)
        else:
            raise ValueError('"playlist_data" deve conter as colunas "Song" e "Artist"')

        count = Counter(all_songs_lyrics).most_common(top)
        count_df = pd.DataFrame(count)
        count_df.columns = ['Word', 'Frequency']
        return count_df


if __name__ == '__main__':
    spotify = Spotify()
    playlist = spotify.get_playlist_content('7CjzoTS4zIhYAfQK50tmvq')
    words = spotify.get_playlist_words(playlist, top=100)
    print()
