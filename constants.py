import numpy as np
from enum import IntEnum



#lsb (least significant bit) msb (most significant bit) trailing zero count trick
debruijn = np.uint64(0x03f79d71b4cb0a89)

lsb_lookup = np.array(
        [ 0,  1, 48,  2, 57, 49, 28,  3,
         61, 58, 50, 42, 38, 29, 17,  4,
         62, 55, 59, 36, 53, 51, 43, 22,
         45, 39, 33, 30, 24, 18, 12,  5,
         63, 47, 56, 27, 60, 41, 37, 16,
         54, 35, 52, 21, 44, 32, 23, 11,
         46, 26, 40, 15, 34, 20, 31, 10,
         25, 14, 19,  9, 13,  8,  7,  6],
        dtype=np.uint8)

msb_lookup = np.array(
        [ 0, 47,  1, 56, 48, 27,  2, 60,
         57, 49, 41, 37, 28, 16,  3, 61,
         54, 58, 35, 52, 50, 42, 21, 44,
         38, 32, 29, 23, 17, 11,  4, 62,
         46, 55, 26, 59, 40, 36, 15, 53,
         34, 51, 20, 43, 31, 22, 10, 45,
         25, 39, 14, 33, 19, 30,  9, 24,
         13, 18,  8, 12,  7,  6,  5, 63],
        dtype=np.uint8)

def lsb_bitscan(bb):
    return lsb_lookup[((bb & -bb) * debruijn) >> np.uint8(58)]

def msb_bitscan(bb):
    bb |= bb >> np.uint8(1)
    bb |= bb >> np.uint8(2)
    bb |= bb >> np.uint8(4)
    bb |= bb >> np.uint8(8)
    bb |= bb >> np.uint8(16)
    bb |= bb >> np.uint8(32)
    return msb_lookup[(bb * debruijn) >> np.uint8(58)]

class Color(IntEnum):
    WHITE = 0
    BLACK = 1

class Piece(IntEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def to_char(self):
        if self == Piece.PAWN:
            return 'p'
        elif self == Piece.KNIGHT:
            return 'n'
        elif self == Piece.BISHOP:
            return 'b'
        elif self == Piece.ROOK:
            return 'r'
        elif self == Piece.QUEEN:
            return 'q'
        elif self == Piece.KING:
            return 'k'

class Rank(IntEnum):
    ONE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7

class File(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    F = 5
    G = 6
    H = 7

#Pregenerated hardcoded tables and bitboards
EMPTY_BB = np.uint64(0)

RANKS = np.array(
            [np.uint64(0x00000000000000FF) << np.uint8(8*i) for i in range(8)],
            dtype=np.uint64)
FILES = np.array(
            [np.uint64(0x0101010101010101) << np.uint8(i) for i in range(8)],
            dtype=np.uint64)

RANK_MASKS = np.fromiter(
        (RANKS[i//8] for i in range(64)),
        dtype=np.uint64,
        count=64)

FILE_MASKS = np.fromiter(
        (FILES[i%8] for i in range(64)),
        dtype=np.uint64,
        count=64)

A1H8_DIAG = np.uint64(0x8040201008040201)
H1A8_ANTIDIAG = np.uint64(0x0102040810204080)

CENTER = np.uint64(0x00003C3C3C3C0000)
#helper to compute diag masks from main diagonals
def compute_diag_mask(i):
    diag = 8*(i & 7) - (i & 56)
    north = -diag & (diag >> 31)
    south = diag & (-diag >> 31)
    return (A1H8_DIAG >> np.uint8(south)) << np.uint8(north)

DIAG_MASKS = np.fromiter(
        (compute_diag_mask(i) for i in range(64)),
        dtype=np.uint64,
        count=64)

def compute_antidiag_mask(i):
    diag = 56 - 8*(i & 7) - (i & 56)
    north = -diag & (diag >> 31)
    south = diag & (-diag >> 31)
    return (H1A8_ANTIDIAG >> np.uint8(south)) << np.uint8(north)

ANTIDIAG_MASKS = np.fromiter(
        (compute_antidiag_mask(i) for i in range(64)),
        dtype=np.uint64,
        count=64)


