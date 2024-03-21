import movegen
import eval
import numpy as np

def minimax(board, depth, alpha, beta, transposition_table):
    if depth == 0:
        return eval.evaluate(board)
    score = eval.Score.CHECKMATE.value

    for move in movegen.gen_legal_moves(board):
        new_board = board.apply_move(move)
        score = -minimax(new_board, depth-1, -beta, -alpha, transposition_table)
        if score > beta:
            break
        max_score = max(score, alpha)
    return max_score
    

def move_suggestions(board):
    pass
    