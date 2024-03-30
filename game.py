import chess
import eval
import search
fen = "r2q1rk1/ppp2ppp/2np1n2/1Bb1p3/3PP1b1/2P2N2/PP3PPP/RNBQR1K1 w - - 1 8"
board = chess.Board(fen)
for move in board.legal_moves:
    print(move)
print(search.alphabeta(board, chess.WHITE, 4))
print(search.count)