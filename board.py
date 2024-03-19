import numpy as np
from constants import Rank, File
from square import Square
EMPTY_BB = np.uint64(0)
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

def occupied_squares(bb):
    while bb != EMPTY_BB:
        lsb_square = Square(lsb_bitscan(bb))
        yield lsb_square
        bb ^= lsb_square.to_bitboard()

def pop_count(bb):
    count = np.uint8(0)
    while bb != EMPTY_BB:
        count += np.uint8(1)
        bb &= bb - np.uint64(1)
    return count

def is_set(bb, sq):
    return (sq.to_bitboard() & bb) != EMPTY_BB

def to_str(bb):
    bb_str = []
    for r in reversed(Rank):
        for f in File:
            sq = Square.from_position(r, f)
            if is_set(bb, sq):
                bb_str.append('1')
            else:
                bb_str.append('.')
        bb_str.append('\n')
    return ''.join(bb_str)

def clear_square(bb, sq):
    return (~sq.to_bitboard()) & bb

def set_square(bb, sq):
    return sq.to_bitboard() | bb
    


