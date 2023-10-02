import pygame

from classes.Piece import Piece

class Rook(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'Rook'
        img_path = 'src/assets/pieces/' + self.color + '_rook.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
    
    def get_possible_moves(self, board):
        output = []
        
        moves_north = []
        moves_east = []
        moves_south = []
        moves_west = []
        
        for y in range(self.y)[::-1]:
            moves_north.append(board.get_square_from_pos((self.x, y)))
        for x in range(self.x + 1, 8):
            moves_east.append(board.get_square_from_pos((x, self.y)))
        for y in range(self.y + 1, 8):
            moves_south.append(board.get_square_from_pos((self.x, y)))
        for x in range(self.x)[::-1]:
            moves_west.append(board.get_square_from_pos((x, self.y)))
        
        output.append(moves_north)
        output.append(moves_east)
        output.append(moves_south)
        output.append(moves_west)
        
        return output