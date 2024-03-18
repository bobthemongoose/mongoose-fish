import numpy as np

# Define hexadecimal representations for each row
ROW_1 = 0xFF
ROW_2 = 0xFF00
ROW_3 = 0xFF0000
ROW_4 = 0xFF000000
ROW_5 = 0xFF00000000
ROW_6 = 0xFF0000000000
ROW_7 = 0xFF000000000000
ROW_8 = 0xFF00000000000000

rows = {1: ROW_1, 2: ROW_2, 3: ROW_3, 4: ROW_4, 5: ROW_5, 6: ROW_6, 7: ROW_7, 8: ROW_8}
# Define hexadecimal representations for each column
COL_1 = 0x0101010101010101
COL_2 = COL_1 << 1
COL_3 = COL_1 << 2
COL_4 = COL_1 << 3
COL_5 = COL_1 << 4
COL_6 = COL_1 << 5
COL_7 = COL_1 << 6
COL_8 = COL_1 << 7


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
