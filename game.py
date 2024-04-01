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
            except (chess.InvalidMoveError, chess.IllegalMoveError) as error:
                move = board.parse_uci(input("not valid \n move?\n"))
    else:
        evaluation, move = search.alphabeta(board, 3)
        if player == chess.WHITE:
            print(-evaluation, move)
        else:
            print(evaluation, move)
    board.push(move)
print(board.outcome)
    