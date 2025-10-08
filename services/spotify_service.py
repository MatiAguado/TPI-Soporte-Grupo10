# Trabajamos con la API de Spotify

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# El parametro son las keywords que debemos traer de RAWG
def search_spotify_playlist(keywords):
    # Autenticamos
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
    ))
    results = sp.search(q=keywords, type='playlist', limit=5)
    playlists = [(pl['name'], pl['external_urls']['spotify']) for pl in results['playlists']['items']]
    return playlists
