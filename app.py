# app.py
import os
import time
import logging
from dotenv import load_dotenv
from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from spotipy.oauth2 import SpotifyOAuth
import spotipy

from services.rawg_service import get_game_info
from services.spotify_service import (
    search_spotify_playlists,
    search_top_tracks_for_keywords,
    create_user_playlist,
    add_items_to_playlist
)

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambiar_esto_en_produccion")
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Spotify OAuth config
SPOTIFY_SCOPE = "user-read-private playlist-modify-public playlist-modify-private"
sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=SPOTIFY_SCOPE,
    open_browser=False
)


def _get_token():
    """Devuelve access_token válido o None. Refresca si corresponde."""
    token_info = session.get('token_info', None)
    if not token_info:
        return None

    now = int(time.time())
    expires_at = token_info.get('expires_at', 0)

    if expires_at - now < 60:
        # refrescar
        try:
            logging.info("Refrescando token de Spotify...")
            refreshed = sp_oauth.refresh_access_token(token_info['refresh_token'])
            session['token_info'] = refreshed
            return refreshed['access_token']
        except Exception:
            logging.exception("No se pudo refrescar el token.")
            session.pop('token_info', None)
            return None

    return token_info['access_token']


# --- Rutas --- #

@app.route('/')
def root():
    # Al abrir la app redirigimos al inicio del flujo de autorización
    if 'token_info' in session:
        return redirect(url_for('home'))
    ##return redirect(url_for('authorize'))
    return render_template('login.html')


@app.route('/authorize')
def authorize():
    # Genera la URL para autorizar y redirige (inicia OAuth)
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/callback')
def callback():
    error = request.args.get('error')
    if error:
        flash("Autorización denegada.", "danger")
        return render_template('login.html', error=error)

    code = request.args.get('code')
    try:
        token_info = sp_oauth.get_access_token(code)
        # token_info: dict con access_token, refresh_token, expires_at, ...
        session['token_info'] = token_info
        logging.info("Usuario autenticado correctamente en Spotify.")
        return redirect(url_for('home'))
    except Exception:
        logging.exception("Error obteniendo token de Spotify.")
        flash("Error de autenticación con Spotify.", "danger")
        return render_template('login.html')


@app.route('/home', methods=['GET'])
def home():
    token = _get_token()
    if not token:
        # si no hay token, forzamos nuevo login
        return redirect(url_for('authorize'))
    return render_template('index.html')


@app.route('/buscar', methods=['POST'])
def buscar():
    token = _get_token()
    if not token:
        flash("Sesión inválida. Por favor iniciá sesión nuevamente.", "warning")
        return redirect(url_for('authorize'))

    sp = spotipy.Spotify(auth=token)
    game_input = (request.form.get('game') or '').strip()
    if not game_input:
        flash("Por favor ingresa un videojuego.", "warning")
        return redirect(url_for('home'))

    try:
        name, genres, description = get_game_info(game_input)
        if name:
            keywords = name
            if genres:
                keywords += ' ' + ' '.join(genres[:3])
        else:
            keywords = game_input

        playlists = search_spotify_playlists(sp, keywords)
        # renderizamos index con resultados
        return render_template('index.html', juego=name or game_input,
                               generos=genres, playlists=playlists, descripcion=description)
    except Exception:
        logging.exception("Error al generar playlists a partir de RAWG/Spotify")
        flash('Ocurrió un error generando las playlists. Verificá las credenciales o intentá de nuevo.', 'danger')
        return render_template('index.html')


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    """Crea una playlist en la cuenta del usuario con tracks relacionados a las keywords."""
    token = _get_token()
    if not token:
        flash("Sesión inválida. Por favor iniciá sesión nuevamente.", "warning")
        return redirect(url_for('authorize'))

    sp = spotipy.Spotify(auth=token)
    game_input = (request.form.get('game') or '').strip()
    custom_name = (request.form.get('playlist_name') or '').strip()

    if not game_input:
        flash("Se necesita el nombre del videojuego para crear la playlist.", "warning")
        return redirect(url_for('home'))

    # Generamos keywords como en /buscar
    name, genres, _ = get_game_info(game_input)
    if name:
        keywords = name
        if genres:
            keywords += ' ' + ' '.join(genres[:3])
    else:
        keywords = game_input

    try:
        # Buscar tracks relacionadas a las keywords
        track_uris = search_top_tracks_for_keywords(sp, keywords, limit=30)
        user = sp.current_user()
        playlist_name = custom_name or f"{game_input} — Playlista generada"
        description = f"Playlist generada automáticamente para '{game_input}' (keywords: {keywords})"
        playlist = create_user_playlist(sp, user['id'], playlist_name, description, public=False)

        if track_uris:
            add_items_to_playlist(sp, playlist['id'], track_uris)
            flash(f"Playlist creada: {playlist_name}", "success")
            return redirect(playlist['external_urls']['spotify'])
        else:
            flash("No se encontraron tracks para poblar la playlist.", "warning")
            return redirect(url_for('home'))
    except Exception:
        logging.exception("Error creando playlist en Spotify.")
        flash("Error al crear la playlist en tu cuenta.", "danger")
        return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('_flashes', None)
    session.pop('token_info', None)
    flash('Sesión finalizada.', 'info')
    ## return redirect(url_for('root'))
    return render_template('login.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)
