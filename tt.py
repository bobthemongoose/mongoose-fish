import random
import chess
class transposition_table:
    def __init__(self):
        self.table = {}
    

class ZobristHash:
    def __init__(self):
        self.piece_keys = {}
        for piece in chess.PIECE_TYPES:
            for square in chess.SQUARES:
                key = random.getrandbits(64)
                self.piece_keys[(piece, square)] = key
        self.side_key = random.getrandbits(64)

    def hash(self, board):
        h = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                h ^= self.piece_keys[(piece.piece_type, square)]
        if board.turn == chess.WHITE:
            h ^= self.side_key
        return h

    def update(self, h, move, piece):
        from_square = move.from_square
        to_square = move.to_square
        h ^= self.piece_keys[(piece.piece_type, from_square)]
        h ^= self.piece_keys[(piece.piece_type, to_square)]
        return h ^ self.side_key
