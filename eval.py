import chess.engine


def eval_board(board):
    """Evaluate the board.

    Args:
        board (chess.Board): The board to evaluate.

    Returns:
        str: The evaluation of the board.
    """
    path = "C:/Users/Dell/Desktop/Chess/stockfish/"
    path += "stockfish-windows-x86-64-avx2.exe"
    with chess.engine.SimpleEngine.popen_uci(path) as engine:
        result = engine.analyse(board, chess.engine.Limit(time=0.1))
        best_move = None
        if not chess.engine.PovScore(result["score"], board.turn).is_mate():
            best_move = result["pv"][0]
        # Get best move

        return (
            "White POV: "
            + str(result["score"].white())
            + "Black POV"
            + str(result["score"].black()),
            best_move,
        )
