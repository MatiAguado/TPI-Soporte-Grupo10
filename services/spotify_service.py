# services/spotify_service.py

def search_spotify_playlists(sp, keywords, limit=6):
    """Recibe una instancia spotipy.Spotify y keywords -> devuelve lista (name, url)."""
    q = (keywords or '').strip()
    if not q:
        return []
    results = sp.search(q=q, type='playlist', limit=limit)
    items = results.get('playlists', {}).get('items', [])
    playlists = [(it['name'], it['external_urls']['spotify']) for it in items]
    return playlists


def search_top_tracks_for_keywords(sp, keywords, limit=30):
    """Busca tracks por keywords y retorna lista de URIs (sin duplicados)."""
    q = (keywords or '').strip()
    if not q:
        return []
    # Buscamos tracks (podés ajustar el tipo de query: e.g., f"{keywords} genre:rock")
    results = sp.search(q=q, type='track', limit=min(limit, 50))
    items = results.get('tracks', {}).get('items', [])
    uris = []
    seen = set()
    for it in items:
        uri = it.get('uri')
        if uri and uri not in seen:
            uris.append(uri)
            seen.add(uri)
    return uris[:limit]


def create_user_playlist(sp, user_id, name, description="", public=False):
    """Crea playlist para user_id y devuelve el objeto playlist."""
    return sp.user_playlist_create(user=user_id, name=name, public=public, description=description)


def add_items_to_playlist(sp, playlist_id, uris):
    """Agrega items (URIs) a la playlist; maneja batches de 100 (limit de Spotify)."""
    if not uris:
        return None
    BATCH = 100
    for i in range(0, len(uris), BATCH):
        sp.playlist_add_items(playlist_id, uris[i:i+BATCH])
    return True
