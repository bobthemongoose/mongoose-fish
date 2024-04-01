import chess
import eval
from tt import TranspositionTable, ZobristHash
count = [0, 0]
def minimax(board: chess.Board, color: chess.Color, depth):
    count[0] += 1
    if depth == 0 or not board.legal_moves:
        return eval.eval(board, color)
    if color == chess.WHITE:
        score = -10000
        for move in board.legal_moves:
            board.push(move)
            score = max(score, minimax(board, chess.BLACK, depth - 1))
            board.pop()

        return score
    else:
        score = 10000
        for move in board.legal_moves:
            board.push(move)
            score = min(score, minimax(board, chess.WHITE, depth - 1))
            board.pop()
        return score

# def alphabeta(board: chess.Board, depth, alpha = -10000, beta = 10000):
#     count[1] += 1
#     if depth == 0 or not board.legal_moves:
#         return eval.eval(board)
#     if board.turn == chess.WHITE:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board,  depth - 1, alpha, beta)
#             board.pop()
#             if score >= beta:
#                 return beta
#             alpha = max(score, alpha)
#         return alpha
#     else:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board,  depth - 1, alpha, beta)
#             board.pop()
#             if score <= alpha:
#                 return alpha
#             beta = min(score, beta)
#         return beta
zobrist_hash = ZobristHash()
transposition_table = TranspositionTable(zobrist_hash)  # Initialize the transposition table


# def alphabeta(board: chess.Board, depth, alpha=-10000, beta=10000, key = None):
#     global transposition_table  # Assuming TranspositionTable is a global variable
#     global zobrist_hash

#     # Check if the position is already stored in the transposition table
#     if not key:
#         key = zobrist_hash.hash(board)
#     table_entry = transposition_table.table.get(key)
#     if table_entry and table_entry[1] >= depth:
#         count[1] += 1
#         return table_entry[0], table_entry[2]  # Return the evaluation score and best move

#     count[0] += 1
    
#     # Evaluate the position if it's a leaf node or depth is zero
#     if depth == 0 or not board.legal_moves:
#         # score = eval.eval(board)
#         score = q_search(board, alpha, beta)
#         # if board.turn == chess.WHITE:
#         #     score = q_search(board, alpha, beta, key)
#         # else:
#         #     score = q_search(board, -beta, -alpha, key)
#         transposition_table.add_key(key, score, depth, None)  # Store the evaluation score
#         return score, None

#     best_move = None
#     if board.turn == chess.WHITE:
#         max_score = -100000
#         for move in board.legal_moves:
#             move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
#             board.push(move)
#             score, _ = alphabeta(board, depth - 1, alpha, beta, move_hash)
#             board.pop()

#             # Update alpha and beta
            
#             if score >= beta:
#                 transposition_table.add_key(key, beta, depth, move)  # Store the evaluation score and best move
#                 return beta, move
#             if score > max_score:
#                 best_move = move
#                 max_score = score
#             alpha = max(score, alpha)
#         transposition_table.add_key(key, alpha, depth, best_move)  # Store the evaluation score and best move
#         return alpha, best_move

#     else:
#         min_score = 100000
#         for move in board.legal_moves:
#             move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
#             board.push(move)
#             score, _ = alphabeta(board, depth - 1, alpha, beta, move_hash)
#             board.pop()
            
#             # Update alpha and beta
            
#             if score <= alpha:
#                 transposition_table.add_key(key, alpha, depth, move)  # Store the evaluation score and best move
#                 return alpha, move
#             if score < min_score:
#                 best_move = move
#                 min_score = score
#             beta = min(score, beta)
#         transposition_table.add_key(key, beta, depth, best_move)  # Store the evaluation score and best move
#         return beta, best_move
def alphabeta(board: chess.Board, depth, alpha=-10000, beta=10000, key = None):
    global transposition_table  # Assuming TranspositionTable is a global variable
    global zobrist_hash

    # Check if the position is already stored in the transposition table
    if not key:
        key = zobrist_hash.hash(board)
    table_entry = transposition_table.table.get(key)
    if table_entry and table_entry[1] >= depth:
        count[1] += 1
        return table_entry[0], table_entry[2]  # Return the evaluation score and best move

    count[0] += 1
    
    # Evaluate the position if it's a leaf node or depth is zero
    if depth == 0 or not board.legal_moves:
        # score = eval.eval(board)
        score = q_search(board, alpha, beta)
        # if board.turn == chess.WHITE:
        #     score = q_search(board, alpha, beta, key)
        # else:
        #     score = q_search(board, -beta, -alpha, key)
        transposition_table.add_key(key, score, depth, None)  # Store the evaluation score
        return score, None

    best_move = None
    max_score = -100000
    for move in board.legal_moves:
        move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
        board.push(move)
        score, _ = alphabeta(board, depth - 1, -beta, -alpha, move_hash)
        score = -score
        board.pop()

        # Update alpha and beta
            
        if score >= beta:
            transposition_table.add_key(key, beta, depth, move)  # Store the evaluation score and best move
            return beta, move
        if score > max_score:
            best_move = move
            max_score = score
        alpha = max(score, alpha)
    transposition_table.add_key(key, alpha, depth, best_move)  # Store the evaluation score and best move
    return alpha, best_move


def q_search(board: chess.Board, alpha, beta, key = None):
    global transposition_table
    global zobrist_hash
    if not key:
        key = zobrist_hash.hash(board)
    table_entry = transposition_table.table.get(key)

    if table_entry and table_entry[1] == 0:
        return table_entry[0]
    stand_pat = eval.eval(board)
    if stand_pat >= beta:
        return stand_pat
    if stand_pat > alpha:
        alpha = stand_pat
    moves = board.generate_pseudo_legal_captures()
    for move in moves:
        move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
        board.push(move)
        score = -q_search(board, -beta, -alpha, move_hash)
        board.pop()
        if score > stand_pat:
            stand_pat = score
            if score > alpha:
                alpha = score
                if score >= beta:
                    break
    transposition_table.add_key(key, stand_pat, 0, None)
    return stand_pat

