import chess
import constants
def eval(board: chess.Board):
    if len(board.legal_moves) == 0:
        if board.is_checkmate():
            return -10000
        else:
            return 0
    else:
        pass
#mobility heuristic
def mobility_diff(board: chess.Board):
    num_curr_moves = len(board.legal_moves)
    board.turn = not board.turn
    num_opp_moves = len(board.legal_moves)
    board.turn = not board.turn
    return num_curr_moves-num_opp_moves

def squares_controlled_by_piece(board, square):
    return len(board.attacks(square))

def piece_type_value(board: chess.Board, color: chess.Color):
    sum = 0
    piece_set = board.pieces(board, color)
    for square in piece_set:
        sum += len(board.attacks(square))
    return sum
#weighing square control by inverse of value of piece (ideally use less valuable pieces to control squares)
def calculate_weighted_scores(board: chess.Board, color: chess.Color):
    weighted_sum = 0
    for piece in constants.piece_types.keys:
        weighted_sum += piece_type_value(board, color) / constants.piece_types[piece]
    return weighted_sum    


    

        

