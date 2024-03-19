import numpy as np
from enum import IntEnum
from square import Square
import board


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


#King Moves

def gen_king_moves(pos):
    square = Square(pos)
    bitboard = square.to_bitboard()
    #directions
    nw = (bitboard & ~FILES[File.A]) << np.uint8(7)
    n = bitboard << np.uint8(8)
    ne = (bitboard & ~FILES[File.H]) << np.uint(9)
    e = (bitboard & ~FILES[File.H]) << np.uint(1)
    w = (bitboard & ~FILES[File.A]) >> np.uint8(1)
    se  = (bitboard & ~FILES[File.H]) >> np.uint8(7)
    s = bitboard >> np.uint(8)
    sw = (bitboard & ~FILES[File.A]) >> np.uint(9)

    return nw | n | ne | e | se | s | sw | w

KING_MOVES = np.fromiter((gen_king_moves(pos) for pos in range(64)), dtype = np.uint(64), count = 64)

#Knight Moves
def gen_knight_moves(pos):
    square = Square(pos)
    bitboard = square.to_bitboard()

    #edge limiting positions

    m1 = ~(FILES[File.A] | FILES[File.B])
    m2 = ~FILES[File.A]
    m3 = ~FILES[File.H]
    m4 = ~(FILES[File.H] | FILES[File.G])
    #directional squares
    sq1 = (bitboard & m1) << np.uint8(6)
    sq2 = (bitboard & m2) << np.uint8(15)
    sq3 = (bitboard & m3) << np.uint8(17)
    sq4 = (bitboard & m4) << np.uint8(10)
    sq5 = (bitboard & m4) >> np.uint8(6)
    sq6 = (bitboard & m3) >> np.uint8(15)
    sq7 = (bitboard & m2) >> np.uint8(17)
    sq8 = (bitboard & m1) >> np.uint8(10)

    return sq1 | sq2 | sq3 | sq4 | sq5 | sq6 | sq7 | sq8

KNIGHT_MOVES = np.fromiter((gen_knight_moves(pos) for pos in range(64)), dtype = np.uint(64), count = 64)

#Pawn non-attack moves
def gen_pawn_na_moves(color, pos):
    start_rank = RANKS[Rank.TWO] if color == Color.WHITE else RANKS[Rank.SEVEN]
    square = Square(pos)
    bitboard = square.to_bitboard
    #forward function
    forward = lambda bb, color, pos: bb << np.uint(8 * pos) if color == Color.WHITE else bb << np.uint(8 * pos)
    sq1 = forward(bitboard, color, 1)
    sq2 = forward((bitboard & start_rank), color, 2)
    return sq1 | sq2

PAWN_NA = np.fromiter((gen_pawn_na_moves(color, i) for color in Color for i in range(64)), dtype= np.uint64, count = 128)
PAWN_NA.shape = (2, 64)

#Pawn attacks
def gen_pawn_attacks(color, pos):
    square = Square(i)
    bitboard = square.to_bitboard()

    if color == Color.WHITE:
        sq1 = (bitboard & ~FILES[File.A]) << np.uint8(7)
        sq2 = (bitboard & ~FILES[File.H]) << np.uint8(9)
    else:
        sq1 = (bitboard & ~FILES[File.A]) >> np.uint8(9)
        sq2 = (bitboard & ~FILES[File.H]) >> np.uint8(7)
    
    return sq1 | sq2

PAWN_ATTACKS = np.fromiter((gen_pawn_attacks(color, pos) for color in Color for pos in range(64)), dtype = np.uint64, count = 128)
PAWN_ATTACKS.shape = (2, 64)

#first rank moves (double step) also check whether blocked or not
def compute_first_rank_moves(i, occ):
    # i is square index from 0 to 8
    # occ is 8-bit number that represents occupancy of the rank 
    # Returns first rank moves (as uint8)

    left_ray = lambda x: x - np.uint8(1)
    right_ray = lambda x: (~x) & ~(x - np.uint8(1))

    x = np.uint8(1) << np.uint8(i)
    occ = np.uint8(occ)

    left_attacks = left_ray(x)
    left_blockers = left_attacks & occ
    if left_blockers != np.uint8(0):
        leftmost = np.uint8(1) << msb_bitscan(np.uint64(left_blockers))
        left_garbage = left_ray(leftmost)
        left_attacks ^= left_garbage

    right_attacks = right_ray(x)
    right_blockers = right_attacks & occ
    if right_blockers != np.uint8(0):
        rightmost = np.uint8(1) << lsb_bitscan(np.uint64(right_blockers))
        right_garbage = right_ray(rightmost)
        right_attacks ^= right_garbage

    return left_attacks ^ right_attacks



FIRST_RANK_MOVES = np.fromiter(
        (compute_first_rank_moves(i, occ)
            for i in range(8) # 8 squares in a rank 
            for occ in range(256)), # 2^8 = 256 possible occupancies of a rank
        dtype=np.uint8,
        count=8*256)
FIRST_RANK_MOVES.shape = (8,256)

