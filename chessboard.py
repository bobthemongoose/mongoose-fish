import numpy as np
from constants import Color
class ChessBoard():
    def __init__(self):
        self.pieces = np.zeros((2, 6), dtype = np.uint64)
        self.color_combined = np.zeros(2, dtype=np.uint64)
        self.all_combined = np.zeros(2, dtype=np.uint64)
        self.color = Color.WHITE