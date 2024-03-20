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
    CONTROL = np.int32(0)
    TEMPO = np.in32(0)
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

def eval_space(board):
    pass

def eval_mobility(board): #perhaps eval per piece and modify piece value based off mobility
    s1_moves = len(movegen.gen_legal_moves(board))
    board.color = ~board.color
    s2_moves = len(movegen.gen_legal_moves(board))
    board.color = ~board.color
    return s1_moves-s2_moves

def eval_num_forcing_moves(board):
    pass
def eval_king_safety(board):
    pass
