"""The main file for the application."""

import chess
import chess.engine
import chess.pgn
import chess.svg
from flask import Flask, render_template

from eval import eval_board
from get_games import get_games

app = Flask("testapp")


class GameState:
    """A class to store the state of the application."""

    def __init__(self):
        self.svgs = []
        self.svgs_flip = []
        self.games = []
        self.curr_game = None
        self.move = 0
        self.moves = []
        self.flip = False  # False for white, True for black
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
        self.get_moves_from_to_format()

    def set_svgs(self):
        """Set the SVGs for the game.

        Args:
            board (chess.Board): The board of the game.
        """
        self.get_moves_from_to_format()
        board = chess.Board()
        evalBoard, best_move = eval_board(board)
        self.svgs = [[chess.svg.board(board), evalBoard, best_move]]
        flipped = chess.svg.board(board, flipped=True)
        self.svgs_flip = [[flipped, evalBoard, best_move]]
        for i in range(len(self.curr_game["moves"])):
            move = self.curr_game["moves"][i]
            from_square = self.coord_to_square(self.moves[i][:2])
            to_square = self.coord_to_square(self.moves[i][2:])
            move_from_to = chess.Move(from_square, to_square)
            board.push_san(move)
            evalBoard = eval_board(board)
            svg = chess.svg.board(board, lastmove=move_from_to)
            self.svgs.append([svg, evalBoard, best_move])
            flipb = chess.svg.board(board, lastmove=move_from_to, flipped=True)
            self.svgs_flip.append([flipb, evalBoard, best_move])

    def flip_board(self):
        """Flip the board."""
        self.flip = not self.flip
        if self.flip:
            self.variable = self.svgs_flip[self.move][0]
        else:
            self.variable = self.svgs[self.move][0]

    def get_moves_from_to_format(self):
        """Get the moves from-to format of the game."""
        board = chess.Board()
        temp = None
        curr = None
        moves = []
        for move in self.curr_game["moves"]:
            temp = board.piece_map()
            board.push_san(move)
            curr = board.piece_map()
            diff = set(temp.items()) ^ set(curr.items())
            moves.append(self.process_diff(diff, move))
        self.moves = moves

    def square_to_coord(self, square):
        """Convert a square to a coordinate.

        Args:
            square (int): The square to convert.

        Returns:
            str: The coordinate of the square.
        """
        return chess.square_name(square)

    def coord_to_square(self, coord):
        """Convert a coordinate to a square.

        Args:
            coord (str): The coordinate to convert.

        Returns:
            int: The square of the coordinate.
        """
        return chess.parse_square(coord)

    def process_diff(self, diff, curr_move):
        """Process the difference between two board states.

        Args:
            diff (set): The difference between two board states.
        """
        if len(diff) == 4:
            a = [item for item in diff if item[1].symbol().lower() == "k"]
            last_move = None
            current_move = None
            if a[1][0] == 4:
                last_move = "e1"
                current_move = self.square_to_coord(a[0][0])
            else:
                last_move = "e8"
                current_move = self.square_to_coord(a[0][0])
            move = last_move + current_move
            return move
        elif len(diff) == 3:
            symbol1 = ""
            symbol2 = ""
            symbol = ""
            for item in diff:
                if symbol1 == "":
                    symbol1 = item[1].symbol().lower()
                else:
                    if symbol1 != item[1].symbol().lower() and symbol2 == "":
                        symbol2 = item[1].symbol().lower()
                    elif symbol1 == item[1].symbol().lower():
                        symbol = item[1].symbol().lower()
                        break
                    elif symbol2 == item[1].symbol().lower():
                        symbol = item[1].symbol().lower()
                        break
            a = [item for item in diff if item[1].symbol().lower() == symbol]
            if (
                curr_move[len(curr_move) - 1] == "+"
                or curr_move[len(curr_move) - 1] == "#"
            ):
                temp_move = self.coord_to_square(
                    curr_move[len(curr_move) - 3: len(curr_move) - 1]
                )
            else:
                temp_move = curr_move[len(curr_move) - 2:]
                temp_move = self.coord_to_square(temp_move)
            if a[0][0] == temp_move:
                from_square = self.square_to_coord(a[1][0])
                to_square = self.square_to_coord(a[0][0])
                move = from_square + to_square
            else:
                from_square = self.square_to_coord(a[0][0])
                to_square = self.square_to_coord(a[1][0])
                move = from_square + to_square
            return move
        else:
            symbol = ""
            for item in diff:
                symbol = item[1].symbol().lower()
            a = [item for item in diff if item[1].symbol().lower() == symbol]
            if (
                curr_move[len(curr_move) - 1] == "+"
                or curr_move[len(curr_move) - 1] == "#"
            ):
                temp_move = self.coord_to_square(
                    curr_move[len(curr_move) - 3: len(curr_move) - 1]
                )
            else:
                temp_move = curr_move[len(curr_move) - 2:]
                temp_move = self.coord_to_square(temp_move)
            if a[0][0] == temp_move:
                from_square = self.square_to_coord(a[0][0])
                to_square = self.square_to_coord(a[1][0])
                move = from_square + to_square
            else:
                from_square = self.square_to_coord(a[1][0])
                to_square = self.square_to_coord(a[0][0])
                move = from_square + to_square
            return move


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
    state.variable = state.svgs[state.move][0]
    return render_template(
        "index.html",
        variable=state.variable,
        eval=state.svgs[state.move][1],
        best_move=state.svgs[state.move][2],
    )


@app.route("/game/<idx>/next")
def next_move(idx):
    """Get the next move in the game.

    Returns:
        str: The rendered HTML of the game page.
    """
    state.move += 1
    state.move = min(len(state.svgs) - 1, state.move)
    if state.flip:
        state.variable = state.svgs_flip[state.move][0]
    else:
        state.variable = state.svgs[state.move][0]
    return render_template(
        "index.html",
        variable=state.variable,
        eval=state.svgs[state.move][1],
        best_move=state.svgs[state.move][2],
    )


@app.route("/game/<idx>/prev")
def prev_move(idx):
    """Get the previous move in the game.

    Returns:
        str: The rendered HTML of the game page.
    """
    state.move -= 1
    state.move = max(0, state.move)
    if state.flip:
        state.variable = state.svgs_flip[state.move][0]
    else:
        state.variable = state.svgs[state.move][0]
    return render_template(
        "index.html",
        variable=state.variable,
        eval=state.svgs[state.move][1],
        best_move=state.svgs[state.move][2],
    )


@app.route("/game/<idx>/flip")
def flip(idx):
    """Flip the board.

    Returns:
        str: The rendered HTML of the home page.
    """
    state.flip_board()
    return render_template(
        "index.html",
        variable=state.variable,
        eval=state.svgs[state.move][1],
        best_move=state.svgs[state.move][2],
    )


if __name__ == "__main__":
    app.run(debug=True)
