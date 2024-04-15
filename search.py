import chess
import eval
from tt import TranspositionTable, ZobristHash, Flag
count = [0, 0]
# def minimax(board: chess.Board, color: chess.Color, depth):
#     count[0] += 1
#     if depth == 0 or not board.legal_moves:
#         return eval.eval(board, color)
#     if color == chess.WHITE:
#         score = -10000
#         for move in board.legal_moves:
#             board.push(move)
#             score = max(score, minimax(board, chess.BLACK, depth - 1))
#             board.pop()

#         return score
#     else:
#         score = 10000
#         for move in board.legal_moves:
#             board.push(move)
#             score = min(score, minimax(board, chess.WHITE, depth - 1))
#             board.pop()
#         return score


zobrist_hash = ZobristHash()
transposition_table = TranspositionTable(zobrist_hash)  # Initialize the transposition table


def alphabeta(board: chess.Board, depth, alpha=-10000, beta=10000, key = None):
    global transposition_table  # Assuming TranspositionTable is a global variable
    global zobrist_hash

    # Check if the position is already stored in the transposition table
    if not key:
        key = zobrist_hash.hash(board)
    table_entry = transposition_table.table.get(key)

    if table_entry and table_entry[1] >= depth:
        count[1] += 1
        if table_entry[3] == Flag.LOWERBOUND:
            alpha = max(alpha, table_entry[0])
        elif table_entry[3] == Flag.UPPERBOUND:
            beta = min(beta, table_entry[0])
        if alpha >= beta:
            return table_entry[0], table_entry[2]  # Return the evaluation score and best move
    in_check = board.is_check()
    if depth >= 3 and not in_check:
            board.push(chess.Move.null())

            score, _ = alphabeta(board, depth - 2, -beta, -beta + 1)
            score = -score
            board.pop()
            if score >= beta:
                if score >= 5000:
                    score = beta

                return score
    count[0] += 1
    old_alpha = alpha
    # Evaluate the position if it's a leaf node or depth is zero
    if depth == 0 or not board.legal_moves:
        # score = eval.eval(board)
        score = q_search(board, alpha, beta)
        # transposition_table.add_key(key, score, depth, None)  # Store the evaluation score
        return score, None

    best_move = None
    max_score = -100000
    moves = sorted(
            board.legal_moves,
            key=lambda move: scoreMove(board, move),
            reverse=True,
        )
    made = 0
    for move in moves:
        made += 1
        move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
        board.push(move)
        score, _ = alphabeta(board, depth - 1, -beta, -alpha, move_hash)
        score = -score
        board.pop()
        made += 1
        # Update alpha and beta
        if score > max_score:
            best_move = move
            max_score = score
            if score > alpha:
                alpha = score
                if score >= beta:
                    break
    if made == 0:
        if in_check:
            return depth - 10000
        else:
            return 0
    if max_score >= beta:
        bound = Flag.LOWERBOUND
    else:
        if alpha != old_alpha:
            bound = Flag.EXACTBOUND
        else:
            bound = Flag.UPPERBOUND
    transposition_table.add_key(key, max_score, depth, best_move, bound)  # Store the evaluation score and best move
        
    
    # transposition_table.add_key(key, alpha, depth, best_move)  # Store the evaluation score and best move
    return max_score, best_move

def translate_score(color: chess.Color, eval):
    if color == chess.WHITE:
        return eval
    else:
        return -eval
    
def q_search(board: chess.Board, alpha, beta, key = None):
    # global transposition_table
    # global zobrist_hash
    # if not key:
    #     key = zobrist_hash.hash(board)
    # table_entry = transposition_table.table.get(key)

    # if table_entry and table_entry[1] == 0:
    #     return table_entry[0]
    stand_pat = eval.eval(board)
    if stand_pat >= beta:
        return stand_pat
    if stand_pat > alpha:
        alpha = stand_pat
    moves = sorted(
            board.generate_legal_captures(),
            key=lambda move: scoreQMove(board, move),
            reverse=True,
        )
    for move in moves:
        # move_hash = zobrist_hash.update(key, move, board.piece_at(move.from_square))
        board.push(move)
        # score = -q_search(board, -beta, -alpha, move_hash)
        score = -q_search(board, -beta, -alpha)
        board.pop()
        if score > stand_pat:
            stand_pat = score
            if score > alpha:
                alpha = score
                if score >= beta:
                    break
    # transposition_table.add_key(key, stand_pat, 0, None)
    return stand_pat

def id_search(board: chess.Board, max_depth):
    for depth in range(1, max_depth + 1):
        score, best_move = alphabeta(board, depth)
        if board.turn == chess.BLACK:
            score = -score
        print(depth, score, best_move)
        
    return score, best_move

#most valuable victim/least valuable aggressor for q search move ordering

def mvvlva(board: chess.Board, move: chess.Move) -> int:
        mvvlva: list[list[int]] = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 105, 104, 103, 102, 101, 100],
            [0, 205, 204, 203, 202, 201, 200],
            [0, 305, 304, 303, 302, 301, 300],
            [0, 405, 404, 403, 402, 401, 400],
            [0, 505, 504, 503, 502, 501, 500],
            [0, 605, 604, 603, 602, 601, 600],
        ]

        from_square = move.from_square
        to_square = move.to_square
        attacker = board.piece_type_at(from_square)
        victim = board.piece_type_at(to_square)

        # En passant
        if victim is None:
            victim = 1
        return mvvlva[victim][attacker]
def scoreQMove(board, move: chess.Move) -> int:
        return mvvlva(board, move)

def scoreMove(board: chess.Board, move: chess.Move) -> int:
    if board.is_capture(move):
        # make sure captures are ordered higher than quiets
        return 10000 + mvvlva(board, move)
    return 0
