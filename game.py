import chess
import eval
import search
import tt
fen = "4k3/8/8/4K3/4P3/8/8/8 w - - 0 1"
board = chess.Board(fen)
# for move in board.legal_moves:
#     print(move)
print(search.alphabeta(board, 15))

print(search.count)
# key = search.zobrist_hash.hash(board)

# move = search.transposition_table.table[key][2]
# inside = True
# print(board)
# while move:
#     print(search.transposition_table.table[key])
#     board.push(move)
#     print(board)
#     key = search.zobrist_hash.hash(board)
#     move = search.transposition_table.table[key][2]
# print()
# print(board)
# print(search.transposition_table.table[search.zobrist_hash.hash(board)])

    