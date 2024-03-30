import chess
import eval

fen = "2K5/8/2PP4/3RPp2/b1p3N1/k2p4/1n2P3/1n2R2B w - - 0 1"
board = chess.Board(fen)
# board.set_board_fen(fen)
print(eval.eval(board))
