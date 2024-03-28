import chess
import constants
def eval(board: chess.Board):
    if len(board.legal_moves) == 0:
        if board.is_checkmate():
            return -10000
        else:
            return 0
#mobility heuristic
def mobility_diff(board: chess.Board):
    num_curr_moves = len(board.legal_moves)
    board.turn = not board.turn
    num_opp_moves = len(board.legal_moves)
    board.turn = not board.turn
    return num_curr_moves-num_opp_moves

def piece_importance(board: chess.Board):
    for piece in chess.PieceType

        

