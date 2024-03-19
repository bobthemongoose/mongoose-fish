import numpy as np
from constants import Color
class Square():
    def __init__(self, index):
        self.index = np.uint8(index)

    def to_bitboard(self):
        return np.uint64(1) << self.index