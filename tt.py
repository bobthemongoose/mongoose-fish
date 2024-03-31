import random
import chess
class ZobristHash:
    def __init__(self):
        self.piece_keys = {}
        for piece_type in chess.PIECE_TYPES:
            for square in chess.SQUARES:
                for color in chess.COLORS:
                    key = random.getrandbits(64)
                    self.piece_keys[(piece_type, square, color)] = key
        self.side_key = random.getrandbits(64)

    def hash(self, board: chess.Board):
        h = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                h ^= self.piece_keys[(piece.piece_type, square, piece.color)]
        if board.turn == chess.WHITE:
            h ^= self.side_key
        return h

    def update(self, h, move, piece):
        from_square = move.from_square
        to_square = move.to_square
        color = piece.color
        h ^= self.piece_keys[(piece.piece_type, from_square, color)]
        if move.promotion is not None:
            promoted_piece = move.promotion
            h ^= self.piece_keys[(promoted_piece, to_square, color)]
        else:
            h ^= self.piece_keys[(piece.piece_type, to_square, color)]
        return h ^ self.side_key

class TranspositionTable:
    def __init__(self, zh: ZobristHash):
        self.table = {}
        self.zh = zh

    def add(self, board, eval_score, depth, best_move):
        key = self.zh.hash(board)
        if (key not in self.table) or (self.table[key][1] < depth):
            self.table[key] = (eval_score, depth, best_move)
     
    def add_key(self, key, eval_score, depth, best_move):
        if (key not in self.table) or (self.table[key][1] < depth):
            self.table[key] = (eval_score, depth, best_move)


