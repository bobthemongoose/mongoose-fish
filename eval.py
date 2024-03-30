import chess
import constants
def eval(board: chess.Board, color: chess.Color):
    count = 0
    for move in board.legal_moves:
        count += 1
    if count == 0:
        if board.is_checkmate():
            if color == chess.WHITE:
                return -10000
            else:
                return 10000
        else:
            return 0
    else:
        score = count_material(board, chess.WHITE) - count_material(board, chess.BLACK)
        # score += mobility_diff * constants.mob_factor
        score += (calculate_weighted_scores(board, chess.WHITE) - calculate_weighted_scores(board, chess.BLACK)) * constants.ctrl_factor
        return score
#mobility heuristic
def mobility_diff(board: chess.Board):
    num_curr_moves = len(board.generate_legal_moves())
    board.turn = not board.turn
    num_opp_moves = len(board.generate_legal_moves())
    board.turn = not board.turn
    return num_curr_moves-num_opp_moves

def squares_controlled_by_piece(board: chess.Board, square: chess.Square):
    return len(board.attacks(square))

def piece_type_value(board: chess.Board, piece: chess.Piece, color: chess.Color):
    sum = 0
    piece_set = board.pieces(piece, color)
    for square in piece_set:
        sum += len(board.attacks(square))
    return sum
#weighing square control by inverse of value of piece (ideally use less valuable pieces to control squares)
def calculate_weighted_scores(board: chess.Board, color: chess.Color):
    weighted_sum = 0
    for piece in constants.piece_types.keys():
        weighted_sum += piece_type_value(board, piece, color) / constants.piece_types[piece]
    return weighted_sum    

def count_material(board: chess.Board, color: chess.Color):
    sum = 0
    for piece in constants.piece_types.keys():
        sum+= len(board.pieces(piece, color)) * constants.piece_types[piece]
    return sum / 100

    

        

