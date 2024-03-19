import numpy as np
from constants import Color, File, Rank, Piece
import board
from square import Square

class ChessBoard():
    def __init__(self):
        self.pieces = np.zeros((2, 6), dtype = np.uint64)
        self.color_combined = np.zeros(2, dtype=np.uint64)
        self.all_combined = np.zeros(2, dtype=np.uint64)
        self.color = Color.WHITE

    def  __str__(self):
        board_str = []
        for r in reversed(Rank):
            for f in File:
                sq = Square.from_position(r, f)
                white_piece = self.piece_on(sq, Color.WHITE)
                black_piece = self.piece_on(sq, Color.BLACK)
                if white_piece is not None:
                    board_str.append(white_piece.to_char().upper())
                elif black_piece is not None:
                    board_str.append(black_piece.to_char())
                else:
                    board_str.append('.')
            board_str.append('\n')
        board_str = ''.join(board_str)
        info_str = "%s to move" % self.color.name
        return "%s%s" % (board_str, info_str)
    
    def get_piece_bb(self, piece, color=None):
        # NOTE: Defaults to current color
        if color is None:
            color = self.color
        return self.pieces[color][piece]

    def piece_on(self, sq, color=None):
        # NOTE: Defaults to current color
        if color is None:
            color = self.color
        return next(
            (p for p in Piece if 
                bitboard.is_set(self.get_piece_bb(p, color), sq)),
            None)

    def set_square(self, sq, piece, color=None):
        # NOTE: Defaults to current color
        if color is None:
            color = self.color
        piece_bb = self.get_piece_bb(piece, color)
        combined_bb = self.combined_color[color]
        all_bb = self.combined_all

        self.pieces[color][piece] = bitboard.set_square(piece_bb, sq)
        self.combined_color[color] = bitboard.set_square(combined_bb, sq)
        self.combined_all = bitboard.set_square(all_bb, sq)

    def clear_square(self, sq, color=None):
        # NOTE: Defaults to current color
        if color is None:
            color = self.color

        piece = self.piece_on(sq, color)
        if piece is None:
            return

        piece_bb = self.get_piece_bb(piece, color)
        combined_bb = self.combined_color[color]
        all_bb = self.combined_all

        self.pieces[color][piece] = bitboard.clear_square(piece_bb, sq)
        self.combined_color[color] = bitboard.clear_square(combined_bb, sq)
        self.combined_all = bitboard.clear_square(all_bb, sq)

    def apply_move(self, move):
        """
        Applies move to chess board
        Returns a new board, doesn't modify original
        """
        new_board = ChessBoard()
        new_board.pieces = np.copy(self.pieces)
        new_board.combined_color = np.copy(self.combined_color)
        new_board.combined_all = np.copy(self.combined_all)
        new_board.color = self.color

        piece = self.piece_on(move.src)
        new_board.clear_square(move.src)
        new_board.clear_square(move.dest, ~new_board.color) # in event of a capture
        new_board.set_square(move.dest, piece if move.promo is None else move.promo)
        
        new_board.color = ~new_board.color
        return new_board


    def init_game(self):
        self.pieces[Color.WHITE][Piece.PAWN] = np.uint64(0x000000000000FF00)
        self.pieces[Color.WHITE][Piece.KNIGHT] = np.uint64(0x0000000000000042)
        self.pieces[Color.WHITE][Piece.BISHOP] = np.uint64(0x0000000000000024)
        self.pieces[Color.WHITE][Piece.ROOK] = np.uint64(0x0000000000000081)
        self.pieces[Color.WHITE][Piece.QUEEN] = np.uint64(0x0000000000000008)
        self.pieces[Color.WHITE][Piece.KING] = np.uint64(0x0000000000000010)

        self.pieces[Color.BLACK][Piece.PAWN] = np.uint64(0x00FF000000000000)
        self.pieces[Color.BLACK][Piece.KNIGHT] = np.uint64(0x4200000000000000)
        self.pieces[Color.BLACK][Piece.BISHOP] = np.uint64(0x2400000000000000)
        self.pieces[Color.BLACK][Piece.ROOK] = np.uint64(0x8100000000000000)
        self.pieces[Color.BLACK][Piece.QUEEN] = np.uint64(0x0800000000000000)
        self.pieces[Color.BLACK][Piece.KING] = np.uint64(0x1000000000000000)

        for p in Piece:
            for c in Color:
                self.combined_color[c] |= self.pieces[c][p]

        self.combined_all = self.combined_color[Color.WHITE] | self.combined_color[Color.BLACK]