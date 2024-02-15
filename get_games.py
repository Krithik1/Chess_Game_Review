"""Get the games for a given user, year, and month."""

import re

from chessdotcom import Client, get_player_games_by_month_pgn

Client.request_config["headers"][
    "User-Agent"
] = "My Python Application. Contact me at email@example.com"


def get_games(username, year, month):
    """Get the games for a given user, year, and month.

    Args:
        username (str): The username of the player.
        year (str): The year of the games.
        month (str): The month of the games.

    Returns:
        list: The list of games for the given user, year, and month.
    """
    data = get_player_games_by_month_pgn(username, year=int(year), month=int(month))
    data = data.json["pgn"]["pgn"]  # pylint: disable=maybe-no-member
    data = data.split('[Event "Live Chess"]')[1:]
    games = []
    for game in data:
        games.append(parse_game(game))
    return games


def parse_game(game):
    """Parse the game into a dictionary.

    Args:
        game (str): The game to parse.

    Returns:
        dict: The parsed game.
    """
    d = {}
    # Index is a hash of the game and is unique and positive
    d["index"] = hash(game) % (10**8)
    d["white"] = game.split('[White "')[1].split('"]')[0]
    d["whiteRating"] = game.split('[WhiteElo "')[1].split('"]')[0]
    d["black"] = game.split('[Black "')[1].split('"]')[0]
    d["blackRating"] = game.split('[BlackElo "')[1].split('"]')[0]
    d["result"] = game.split('[Result "')[1].split('"]')[0]
    d["date"] = game.split('[Date "')[1].split('"]')[0]
    d["termination"] = game.split('[Termination "')[1].split('"]')[0]
    d["moves"] = game.split("\n1. ")[1].split(" " + d["result"])[0]
    d["moves"] = re.sub(r"\{[^{}]*\}", "", d["moves"]).strip(" ")
    d["moves"] = re.sub(r"\d+\.+", "", d["moves"]).split(" ")
    d["moves"] = [move for move in d["moves"] if move != ""]
    return d
