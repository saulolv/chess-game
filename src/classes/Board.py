import pygame

import Square
from classes.pieces import Rook, Knight, Bishop, Queen, King, Pawn

# Game state checker
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = self.width // 8
        self.tile_height = self.height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            [Rook(0, 0, 'black'), Knight(1, 0, 'black'), Bishop(2, 0, 'black'), Queen(3, 0, 'black'), King(4, 0, 'black'), Bishop(5, 0, 'black'), Knight(6, 0, 'black'), Rook(7, 0, 'black')],
            [Pawn(i, 1, 'black') for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [None for i in range(8)],
            [Pawn(i, 6, 'white') for i in range(8)],
            [Rook(0, 7, 'white'), Knight(1, 7, 'white'), Bishop(2, 7, 'white'), Queen(3, 7, 'white'), King(4, 7, 'white'), Bishop(5, 7, 'white'), Knight(6, 7, 'white'), Rook(7, 7, 'white')]
        ]
        self.squares = self.create_squares()
        self.setup_board()
    
    def generate_squares(self):
        output = []
        for y in range(8):
            for x in range(8):
                output.append(Square(x, y, self.tile_width, self.tile_height))
        return output
    
    def get_square_from_pos(self, pos):
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square
    
    def get_piece_from_pos(self, pos):
        return self.get_square_from_pos(pos).occupying_piece
    
    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece:
                    square = self.get_square_from_pos((x, y))
                    
                    # looking inside contents, what piece does it have
                    if piece[1] == 'Rook':
                        square.occupying_piece = Rook((x, y), 'white' if piece[0] == 'w' else 'black')
                    
                    elif piece[1] == 'Knight':
                        square.occupying_piece = Knight((x, y), 'white' if piece[0] == 'w' else 'black')
                    
                    elif piece[1] == 'Bishop':
                        square.occupying_piece = Bishop((x, y), 'white' if piece[0] == 'w' else 'black')
                    
                    elif piece[1] == 'Queen':
                        square.occupying_piece = Queen((x, y), 'white' if piece[0] == 'w' else 'black')
                        
                    elif piece[1] == 'King':
                        square.occupying_piece = King((x, y), 'white' if piece[0] == 'w' else 'black')
                    
                    elif piece[1] == 'Pawn':
                        square.occupying_piece = Pawn((x, y), 'white' if piece[0] == 'w' else 'black')
    
    def handle_click(self, mx, my):
        x = mx // self.tile_width
        y = my // self.tile_height
        clicked_square = self.get_square_from_pos((x, y))
        
        if self.selected_piece is None:
            if clicked_square.occupying_piece is not None and clicked_square.occupying_piece.color == self.turn:
                self.selected_piece = clicked_square.occupying_piece
        elif self.selected_piece.move(self, clicked_square):
            self.turn = 'white' if self.turn == 'black' else 'black'
        elif clicked_square.occupying_piece is not None and clicked_square.occupying_piece.color == self.turn:
            self.selected_piece = clicked_square.occupying_piece
     
    # check state checker       
    def is_in_check(self, color, board_change=None):
        output = False
        king_pos = None
        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None
        
        if board_change:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        
        if changing_piece:
            if changing_piece.notation == 'King':
                king_pos = new_square.pos
        if king_pos is None:
            for piece in pieces:
                if piece.notation == 'King' and piece.color == color:
                    king_pos = piece.pos
                    break
        
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True
                        break
        
        if board_change:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
            
        return output
    
    # checkmate state checker
    def is_in_checkmate(self, color):
        output = False
        
        for piece in [i.occupying_piece for i in self.squares]:
            if piece:
                if piece.notation == 'King' and piece.color == color:
                    king = piece
                    break
        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                output = True
        return output
    
    def draw(self, screen):
        if self.selected_piece:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(screen)