import chess
import eval
import search
import tt
board = chess.Board()
color = input("play w/b?\n")
while color not in ("w", "b"):
    color = input("play w/b?\n")
if color == "w":
    player = chess.WHITE
else:
    player = chess.BLACK
while not board.is_game_over():
    print(board)
    if board.turn == player:
        while True:
            try:
                move = board.parse_uci(input("move?\n"))
                break
            except chess.InvalidMoveError:
                move = board.parse_uci(input("move?\n"))
    else:
        evaluation, move = search.alphabeta(board, 4)
        print(evaluation, move)
    board.push(move)
print(board.outcome)
    