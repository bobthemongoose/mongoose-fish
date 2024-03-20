from enum import Enum
import numpy as np
from chessboard import ChessBoard
from constants import Piece
import constants
import board
import movegen

class Score(Enum):
    PAWN = np.int32(100)
    KNIGHT = np.int32(300)
    BISHOP = np.int32(300)
    ROOK = np.int32(500)
    QUEEN = np.int32(900)
    CHECKMATE = np.int32(-1000000)

def evaluate(board):
    return eval_pieces(board)

def piece_diff(board, piece):
    return np.int32(board.pop_count(board.pieces[board.color][piece])) - np.int32(board.pop_count(board.pieces[~board.color][piece]))

def eval_pieces(board):
    return (Score.PAWN.value * piece_diff(board, Piece.PAWN)
        + Score.KNIGHT.value * piece_diff(board, Piece.KNIGHT)
        + Score.BISHOP.value * piece_diff(board, Piece.BISHOP)
        + Score.ROOK.value * piece_diff(board, Piece.ROOK)
        + Score.QUEEN.value * piece_diff(board, Piece.QUEEN))
