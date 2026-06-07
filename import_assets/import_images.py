from import_assets.fetch_images import fetch_game, fetch_game_grids, fetch_game_heroes, fetch_game_cover, fetch_game_banner, fetch_game_logo, write_image
from utils.utils import toUnsigned
from utils.steam_utils import get_steam_id

COVER_EXTENSION = "p"
BACKGROUND_EXTENSION = "_hero"
LOGO_EXTENSION = "_logo"

def import_images(steam_directory, app_id, name):
    user_id = get_steam_id(steam_directory)
    image_id = toUnsigned(app_id)
    print(image_id)
    path = f"{steam_directory}\\userdata\\{user_id}\\config\\grid"

    game = fetch_game(name)
    grids = fetch_game_grids(game.id)
    heroes = fetch_game_heroes(game.id)

    cover_url = fetch_game_cover(game, grids)
    write_image(cover_url, f"{path}\\{image_id}{COVER_EXTENSION}.png")

    cover_url = fetch_game_banner(game, heroes)
    write_image(cover_url, f"{path}\\{image_id}{BACKGROUND_EXTENSION}.png")

    cover_url = fetch_game_logo(game)
    write_image(cover_url, f"{path}\\{image_id}{LOGO_EXTENSION}.png")