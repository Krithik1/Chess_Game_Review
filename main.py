import chess
import chess.engine
import chess.pgn
import chess.svg
from flask import Flask, redirect, render_template, url_for

from getGames import get_games

app = Flask("testapp")
svgs = []
move = 0


def main():
    games = get_games("username")
    print(games[0])
    print(games[0]["moves"])
    print(games[0]["termination"])
    print(games[0]["result"])
    print(games[0]["white"])
    print(games[0]["black"])
    print(games[0]["date"])
    print(games[0]["whiteRating"])
    print(games[0]["blackRating"])
    print(games[0]["index"])
    global svgs
    board = chess.Board()
    svgs.append(board._repr_svg_())
    for move in games[0]["moves"]:
        board.push_san(move)
        svgs.append(board._repr_svg_())
    return svgs[0]


variable = main()


@app.route("/")
def index():
    return render_template("index.html", variable=variable)


@app.route("/next")
def next():
    global svgs
    global move
    global variable
    move += 1
    if move >= len(svgs):
        move = len(svgs) - 1
    variable = svgs[move]
    return render_template("index.html", variable=variable)


@app.route("/prev")
def prev():
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
