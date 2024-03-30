import chess
import eval
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

def alphabeta(board: chess.Board, color: chess.Color, depth, alpha = -10000, beta = 10000):
    count[1] += 1
    if depth == 0 or not board.legal_moves:
        return eval.eval(board, color)
    if color == chess.WHITE:
        for move in board.legal_moves:
            board.push(move)
            score = alphabeta(board, chess.BLACK, depth - 1, alpha, beta)
            board.pop()
            if score >= beta:
                return beta
            alpha = max(score, alpha)
        return alpha
    else:
        for move in board.legal_moves:
            board.push(move)
            score = alphabeta(board, chess.WHITE, depth - 1, alpha, beta)
            board.pop()
            if score <= alpha:
                return alpha
            beta = min(score, beta)
        return beta
