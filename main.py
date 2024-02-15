"""The main file for the application."""

import chess
import chess.engine
import chess.pgn
import chess.svg
from flask import Flask, render_template

from get_games import get_games

app = Flask("testapp")


class GameState:
    """A class to store the state of the application."""

    def __init__(self):
        self.svgs = []
        self.games = []
        self.curr_game = None
        self.move = 0
        self.variable = None

    def find_curr_game(self, idx):
        """Find the current game with the given index.

        Args:
            idx (str): The index of the game.
        """
        for game in self.games:
            if game["index"] == int(idx):
                self.curr_game = game
                break

    def set_svgs(self):
        """Set the SVGs for the game.

        Args:
            board (chess.Board): The board of the game.
        """
        board = chess.Board()
        self.svgs = [chess.svg.board(board)]
        for move in self.curr_game["moves"]:
            board.push_san(move)
            self.svgs.append(chess.svg.board(board))


state = GameState()


@app.route("/")
def index():
    """The home page of the application.

    Returns:
        str: The rendered HTML of the home page.
    """
    return render_template("home.html")


@app.route("/games/<username>/<year>/<month>")
def get_games_html(username, year, month):
    """Get the games for a given user, year, and month.

    Args:
        username (str): The username of the player.
        year (str): The year of the games.
        month (str): The month of the games.

    Returns:
        str: The rendered HTML of the games page.
    """
    state.games = get_games(username, year, month)
    return render_template("games.html", games=state.games, username=username)


@app.route("/game/<idx>")
def get_game(idx):
    """Get the game with the given index.

    Args:
        idx (str): The index of the game.

    Returns:
        str: The rendered HTML of the game page.
    """
    state.find_curr_game(idx)
    state.set_svgs()
    state.move = 0
    state.variable = state.svgs[state.move]
    return render_template("index.html", variable=state.variable)


@app.route("/game/<idx>/next")
def next_move(idx):
    """Get the next move in the game.

    Returns:
        str: The rendered HTML of the game page.
    """
    print(idx)
    state.move += 1
    state.move = min(len(state.svgs) - 1, state.move)
    state.variable = state.svgs[state.move]
    return render_template("index.html", variable=state.variable)


@app.route("/game/<idx>/prev")
def prev_move(idx):
    """Get the previous move in the game.

    Returns:
        str: The rendered HTML of the game page.
    """
    print(idx)
    state.move -= 1
    state.move = max(0, state.move)
    state.variable = state.svgs[state.move]
    return render_template("index.html", variable=state.variable)


if __name__ == "__main__":
    app.run()
