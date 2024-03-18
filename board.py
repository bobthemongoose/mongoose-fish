import numpy as np
import constants
class Board():
    def __init__(self):
        self.white_rook_bitboard = np.uint64(0)
        self.white_bishop_bitboard = np.uint64(0)
        self.white_king_bitboard = np.uint64(0)
        self.white_pawn_bitboard = np.uint64(0)
        self.white_knight_bitboard = np.uint64(0)
        self.white_queen_bitboard = np.uint64(0)

        self.black_rook_bitboard = np.uint64(0)
        self.black_bishop_bitboard = np.uint64(0)
        self.black_king_bitboard = np.uint64(0)
        self.black_pawn_bitboard = np.uint64(0)
        self.black_knight_bitboard = np.uint64(0)
        self.black_queen_bitboard = np.uint64(0) 

    @property
    def white_pieces_bitboard(self):
        return self.white_rook_bitboard | self.white_bishop_bitboard | self.white_king_bitboard | self.white_pawn_bitboard | self.white_knight_bitboard | self.white_queen_bitboard
    @property
    def black_pieces_bitboard(self):
        return self.black_rook_bitboard | self.black_bishop_bitboard | self.black_king_bitboard | self.black_pawn_bitboard | self.black_knight_bitboard | self.black_queen_bitboard

    @property
    def occupied_squares_bitboard(self):
        return self.white_pieces_bitboard | self.black_pieces_bitboard

    @property
    def empty_squares_bitboard(self):
        return ~self.occupied_squares_bitboard
    


