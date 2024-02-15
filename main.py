import chess
import chess.engine
import chess.pgn
import chess.svg
from flask import Flask, render_template

from getGames import get_games

app = Flask("testapp")
svgs = []
games = []
curr_game = None
move = 0
variable = None


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/games/<username>/<year>/<month>")
def games(username, year, month):
    global games
    games = get_games(username, year, month)
    return render_template("games.html", games=games, username=username)


@app.route("/game/<index>")
def game(index):
    global svgs
    global variable
    global move
    global games
    global curr_game
    for game in games:
        if game["index"] == int(index):
            curr_game = game
            break
    board = chess.Board()
    svgs = [board._repr_svg_()]
    for move in curr_game["moves"]:
        board.push_san(move)
        svgs.append(board._repr_svg_())
    move = 0
    variable = svgs[move]
    return render_template("index.html", variable=variable)


@app.route("/game/<index>/next")
def next(index):
    global svgs
    global move
    global variable
    move += 1
    if move >= len(svgs):
        move = len(svgs) - 1
    variable = svgs[move]
    return render_template("index.html", variable=variable)


@app.route("/game/<index>/prev")
def prev(index):
    global svgs
    global move
    global variable
    move -= 1
    if move < 0:
        move = 0
    variable = svgs[move]
    return render_template("index.html", variable=variable)


if __name__ == "__main__":
    app.run()
