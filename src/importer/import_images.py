from utils.load_data import fetch_config
from steam.steam_helpers import get_steam_id, to_unsigned
from api import fetch_images
from pathlib import Path

COVER_EXTENSION = "p"
BACKGROUND_EXTENSION = "_hero"
LOGO_EXTENSION = "_logo"

config = fetch_config()

def import_images(rom):
    user_id = get_steam_id()
    image_id = to_unsigned(rom["appid"])

    path = f"{config["paths"]["steam_path"]}/userdata/{user_id}/config/grid"

    cover_path = f"{path}/{image_id}{COVER_EXTENSION}.png"
    background_path = f"{path}/{image_id}{BACKGROUND_EXTENSION}.png"
    logo_path = f"{path}/{image_id}{LOGO_EXTENSION}.png"

    game, grids, heroes = None, None, None
    if (not Path(cover_path).is_file()
    or not Path(background_path).is_file()
    or not Path(logo_path).is_file()):
        game = fetch_images.fetch_game(rom["appname"])
        grids = fetch_images.fetch_game_grids(game.id)
        heroes = fetch_images.fetch_game_heroes(game.id)

    if not Path(cover_path).is_file():
        cover_url = fetch_images.fetch_game_cover(game, grids)
        fetch_images.write_image(cover_url, cover_path)

    if not Path(background_path).is_file():
        cover_url = fetch_images.fetch_game_banner(game, heroes)
        fetch_images.write_image(cover_url, background_path)

    if not Path(logo_path).is_file():
        cover_url = fetch_images.fetch_game_logo(game)
        fetch_images.write_image(cover_url, logo_path)
