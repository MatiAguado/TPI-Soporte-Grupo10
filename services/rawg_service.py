# services/rawg_service.py
import os
import requests
import logging

RAWG_KEY = os.getenv("RAWG_API_KEY")

def get_game_info(name):
    """Devuelve (name, [genres], description) o (None, [], '')."""
    if not name:
        return None, [], ""
    params = {"key": RAWG_KEY, "search": name}
    try:
        r = requests.get("https://api.rawg.io/api/games", params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])
        if not results:
            return None, [], ""
        game = results[0]
        genres = [g['name'] for g in game.get('genres', [])]
        description = game.get('description_raw') or ""
        return game.get('name'), genres, description
    except Exception:
        logging.exception("Error consultando RAWG")
        return None, [], ""
