# Trabajamos con la API de RAWG

import requests
import os

def get_game_info(name):
    key = os.getenv("RAWG_API_KEY")
    url = f"https://api.rawg.io/api/games?key={key}&search={name}"
    response = requests.get(url).json()
    if response["results"]:
        game = response["results"][0]
        generos = [g["name"] for g in game["genres"]]
        return game["name"], generos, game["slug"]
    return None, [], None
