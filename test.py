import chess
import search
import eval
import timeit

# Define a function that wraps the alphabeta call
def run_alphabeta():
    fen = "rnb1kbnr/pppp1ppp/8/4p3/4P2q/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    board = chess.Board(fen)
    # result = eval.eval(board)
    # result = search.q_search(board, -10000, 10000)
    result = search.alphabeta(board, 2)
    if board.turn != chess.WHITE:
        print(-result[0], result[1])
    else:
        print(result[0], result[1])
    # print(result)
# Time the execution of the function
# execution_time = timeit.timeit(run_alphabeta, number=1)
# print("Execution time:", execution_time, "seconds")

fen = "r2qkn1Q/pbp2p2/2pb4/3ppr2/8/2N1P1P1/PPPP1P1P/R1B1K1NR w KQkq - 0 1"
board = chess.Board(fen)
print(board)
# print(board.is_checkmate())
result = search.alphabeta(board, 4)
print(result)
# for move in board.legal_moves:
#     board.push(move)
#     print(move)
#     print(search.transposition_table.table[search.zobrist_hash.hash(board)])
#     board.pop()
# print(search.transposition_table.table[search.zobrist_hash.hash(board)])