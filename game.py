import chess
import eval
import search
fen = "r1bq2r1/b4pk1/p1pp1p2/1p2pP2/1P2P1PB/3P4/1PPQ2P1/R3K2R w"
board = chess.Board(fen)
print(search.alphabeta(board, chess.WHITE, 4))
print(search.count)