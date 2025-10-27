from flask import Flask, render_template, request
from services.rawg_service import get_game_info
from services.spotify_service import search_spotify_playlist
import os
import logging

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    playlists = None
    error = None
    game = ''

    if request.method == 'POST':
        game = (request.form.get('game') or '').strip()
        if not game:
            error = 'Por favor, ingresa un videojuego.'
        else:
            try:
                # Intentamos enriquecer las keywords con RAWG (nombre + géneros)
                name, genres, slug = get_game_info(game)
                if name:
                    keywords = name
                    if genres:
                        keywords += ' ' + ' '.join(genres[:3])  # limitamos algunos géneros
                else:
                    # Si RAWG no devuelve nada, usamos lo que escribió el usuario
                    keywords = game

                playlists = search_spotify_playlist(keywords)
            except Exception:
                logging.exception('Error al generar playlists a partir de RAWG/Spotify')
                error = 'Ocurrió un error al generar las playlists. Verifica tus credenciales de RAWG/Spotify e inténtalo nuevamente.'

    return render_template('index.html', playlists=playlists, error=error, game=game)


def create_app():
    """Factory opcional para entornos WSGI/servicios en la nube."""
    return app


if __name__ == '__main__':
    # Ejecuta en localhost. Puedes cambiar el puerto mediante la variable de entorno PORT
    port = int(os.getenv('PORT', 5001))
    app.run(host='127.0.0.1', port=port, debug=True)
