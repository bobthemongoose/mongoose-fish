import chess
import constants
def eval(board: chess.Board):
    w_mat = count_material(board, chess.WHITE)
    b_mat = count_material(board, chess.BLACK)
    score = w_mat - b_mat
    score += mobility_diff(board) * constants.mob_factor
    score += (calculate_weighted_scores(board, chess.WHITE) - calculate_weighted_scores(board, chess.BLACK)) * constants.ctrl_factor
    if max(w_mat, b_mat) <= constants.piece_types[chess.KING] + 6 * constants.piece_types[chess.PAWN]:
        if w_mat > b_mat:
            score += mop_up(board, chess.WHITE)
        else:
            score += mop_up(board, chess.BLACK)
    if board.turn == chess.WHITE:
        return score
    
    return -score
#mobility heuristic
def mobility_diff(board: chess.Board):
    num_curr_moves = count_moves(board)
    board.turn = not board.turn
    num_opp_moves = count_moves(board)
    board.turn = not board.turn
    return num_curr_moves-num_opp_moves
def count_moves(board):
    return len(list(board.generate_pseudo_legal_moves()))
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

def mop_up(board: chess.Board, win_color: chess.Color):
    win_king = board.king(win_color)
    lose_king = board.king(not win_color)
    king_dist = chess.square_manhattan_distance(win_king, lose_king)
    return (4.7 * constants.cmd(lose_king) + 1.6 * (14 - king_dist))/50

        

