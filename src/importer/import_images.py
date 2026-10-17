from utils.load_data import fetch_config
from steam.steam_helpers import get_steam_id, to_unsigned
from api import fetch_images

COVER_EXTENSION = "p"
BACKGROUND_EXTENSION = "_hero"
LOGO_EXTENSION = "_logo"

config = fetch_config()

def import_images(rom):
    # steam_id should be get_steam_id(steam_directory)
    # image_id should be to_unassigned(app_id)
    user_id = get_steam_id()
    image_id = to_unsigned(rom["appid"])

    path = f"{config["paths"]["steam_path"]}/userdata/{user_id}/config/grid"

    game = fetch_images.fetch_game(rom["appname"])
    grids = fetch_images.fetch_game_grids(game.id)
    heroes = fetch_images.fetch_game_heroes(game.id)

    cover_url = fetch_images.fetch_game_cover(game, grids)
    fetch_images.write_image(cover_url, f"{path}/{image_id}{COVER_EXTENSION}.png")

    cover_url = fetch_images.fetch_game_banner(game, heroes)
    fetch_images.write_image(cover_url, f"{path}/{image_id}{BACKGROUND_EXTENSION}.png")

    cover_url = fetch_images.fetch_game_logo(game)
    fetch_images.write_image(cover_url, f"{path}/{image_id}{LOGO_EXTENSION}.png")
