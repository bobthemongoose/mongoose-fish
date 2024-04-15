import chess
piece_types = {chess.PAWN: 100, chess.KNIGHT: 325, chess.KING:40000, chess.BISHOP: 325, chess.ROOK: 500, chess.QUEEN: 1050}
colors = [chess.WHITE, chess.BLACK]

mob_factor, ctrl_factor = [0.15, 0.5]

cmd_table = [
  [6, 5, 4, 3, 3, 4, 5, 6],
  [5, 4, 3, 2, 2, 3, 4, 5],
  [4, 3, 2, 1, 1, 2, 3, 4],
  [3, 2, 1, 0, 0, 1, 2, 3],
  [3, 2, 1, 0, 0, 1, 2, 3],
  [4, 3, 2, 1, 1, 2, 3, 4],
  [5, 4, 3, 2, 2, 3, 4, 5],
  [6, 5, 4, 3, 3, 4, 5, 6]
]

def cmd(square: chess.Square):
    return cmd_table[chess.square_file(square)][chess.square_rank(square)]