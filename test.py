import chess
import search
import eval
import timeit

# Define a function that wraps the alphabeta call
def run_alphabeta():
    fen = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1"
    board = chess.Board(fen)
    # result = eval.eval(board)
    # result = search.q_search(board, -10000, 10000)
    result = search.alphabeta(board, 4)
    if board.turn != chess.WHITE:
        print(-result[0], result[1])
    else:
        print(result[0], result[1])
    # print(result)
# Time the execution of the function
execution_time = timeit.timeit(run_alphabeta, number=1)
print("Execution time:", execution_time, "seconds")

