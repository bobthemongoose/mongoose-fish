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

# def alphabeta(board: chess.Board, color: chess.Color, depth, alpha = -10000, beta = 10000):
#     count[1] += 1
#     if depth == 0 or not board.legal_moves:
#         return eval.eval(board, color)
#     if color == chess.WHITE:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board, chess.BLACK, depth - 1, alpha, beta)
#             board.pop()
#             if score >= beta:
#                 return beta
#             alpha = max(score, alpha)
#         return alpha
#     else:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board, chess.WHITE, depth - 1, alpha, beta)
#             board.pop()
#             if score <= alpha:
#                 return alpha
#             beta = min(score, beta)
#         return beta
zobrist_hash = ZobristHash()
transposition_table = TranspositionTable(zobrist_hash)  # Initialize the transposition table

# def alphabeta(board: chess.Board, color: chess.Color, depth, alpha=-10000, beta=10000):
#     global transposition_table  # Assuming TranspositionTable is a global variable
#     global zobrist_hash
#     # Check if the position is already stored in the transposition table
#     table_entry = transposition_table.table.get(zobrist_hash.hash(board))
#     if table_entry is not None and table_entry[1] >= depth:
#         count[1] += 1
#         return table_entry[0]
#     count[0] += 1
#     # Evaluate the position if it's a leaf node or depth is zero
#     if depth == 0 or not board.legal_moves:
#         score = eval.eval(board, color)
#         transposition_table.add(board, score, depth, None)  # Store the evaluation score
#         return score

#     if color == chess.WHITE:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board, chess.BLACK, depth - 1, alpha, beta)
#             board.pop()

#             # Update alpha and beta
#             alpha = max(score, alpha)
#             if score >= beta:
#                 transposition_table.add(board, beta, depth, move)  # Store the evaluation score and best move
#                 return beta
#         transposition_table.add(board, alpha, depth, move)  # Store the evaluation score and best move
#         return alpha

#     else:
#         for move in board.legal_moves:
#             board.push(move)
#             score = alphabeta(board, chess.WHITE, depth - 1, alpha, beta)
#             board.pop()

#             # Update alpha and beta
#             beta = min(score, beta)
#             if score <= alpha:
#                 transposition_table.add(board, alpha, depth, move)  # Store the evaluation score and best move
#                 return alpha
#         transposition_table.add(board, beta, depth, move)  # Store the evaluation score and best move
#         return beta

def alphabeta(board: chess.Board, color: chess.Color, depth, alpha=-10000, beta=10000):
    global transposition_table  # Assuming TranspositionTable is a global variable
    global zobrist_hash

    # Check if the position is already stored in the transposition table
    table_entry = transposition_table.table.get(zobrist_hash.hash(board))
    if table_entry is not None and table_entry[1] >= depth:
        count[1] += 1
        return table_entry[0], table_entry[2]  # Return the evaluation score and best move

    count[0] += 1

    # Evaluate the position if it's a leaf node or depth is zero
    if depth == 0 or not board.legal_moves:
        score = eval.eval(board, color)
        transposition_table.add(board, score, depth, None)  # Store the evaluation score
        return score, None

    best_move = None
    if color == chess.WHITE:
        max_score = alpha
        for move in board.legal_moves:
            board.push(move)
            score, _ = alphabeta(board, chess.BLACK, depth - 1, alpha, beta)
            board.pop()

            # Update alpha and beta
            alpha = max(score, alpha)
            if score >= beta:
                transposition_table.add(board, beta, depth, move)  # Store the evaluation score and best move
                return beta, move
            if score > max_score:
                best_move = move
                max_score = score
        transposition_table.add(board, alpha, depth, best_move)  # Store the evaluation score and best move
        return alpha, best_move

    else:
        min_score = beta
        for move in board.legal_moves:
            board.push(move)
            score, _ = alphabeta(board, chess.WHITE, depth - 1, alpha, beta)
            board.pop()
            
            # Update alpha and beta
            beta = min(score, beta)
            if score <= alpha:
                transposition_table.add(board, alpha, depth, move)  # Store the evaluation score and best move
                return alpha, move
            if score < min_score:
                best_move = move
                min_score = score
        transposition_table.add(board, beta, depth, best_move)  # Store the evaluation score and best move
        return beta, best_move


