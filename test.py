import chess
import search
import timeit

# Define a function that wraps the alphabeta call
def run_alphabeta():
    fen = "rnb1kbnr/pppp1ppp/4p3/8/3PP2q/8/PPP2PPP/RNBQKBNR b KQkq - 0 1"
    board = chess.Board(fen)
    # result = search.q_search(board, -10000, 10000)
    result = search.alphabeta(board, 4)
    print(result)

# Time the execution of the function
execution_time = timeit.timeit(run_alphabeta, number=1)
print("Execution time:", execution_time, "seconds")

