import chess

def eval(board):
    return len(board.legal_moves)