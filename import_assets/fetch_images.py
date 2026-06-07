from steamgrid import SteamGridDB
from dotenv import load_dotenv
import os
import requests

load_dotenv()

sgdb = SteamGridDB(os.getenv("API_KEY"))

def fetch_game(name):
    games = sgdb.search_game(name)
    if not games:
        print(f"{name} not found")
        return
    return games[0]

def fetch_game_grids(game_id):
    return sgdb.get_grids_by_gameid(game_ids=[game_id])

def fetch_game_heroes(game_id):
    return sgdb.get_heroes_by_gameid(game_ids=[game_id])

def fetch_game_banner(game, heroes):
    if not heroes:
        print(f"Cover not found for {game.name}")
        return

    for hero in heroes:
        if hero.width == 1920 and hero.height == 620 or hero.width == 3840 and hero.height == 1240:
            return hero
        
def fetch_game_cover(game, grids):
    if not grids:
        print(f"Cover not found for {game.name}")
        return

    for grid in grids:
        if grid.width == 600 and grid.height == 900:
            return grid

def fetch_game_logo(game):
    game_id = game.id
    logos = sgdb.get_logos_by_gameid(game_ids=[game_id])
    if not logos:
        print(f"Icon not found for {game.name}")
        return
    return logos[0]

def write_image(url, file_path):
    if not url is None:
        img_data = requests.get(url).content
        with open(file_path, 'wb') as img:
            img.write(img_data)