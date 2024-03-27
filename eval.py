import chess
def eval(board: chess.Board):
    if len(board.legal_moves) == 0:
        if board.is_checkmate():
            return -10000
        else:
            return 0
    #mobility heuristic
    num_curr_moves = len(board.legal_moves)
    board.turn = not board.turn
    num_opp_moves = len(board.legal_moves)
    board.turn = not board.turn
    move_diff = num_curr_moves-num_opp_moves

    
        

