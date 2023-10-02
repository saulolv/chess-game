import pygame

from classes.Piece import Piece

class Queen(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'Queen'
        img_path = 'src/assets/pieces/' + self.color + '_queen.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
        
    def get_possible_moves(self, board):
        output = []
        
        moves_north = []
        moves_northeast = []
        moves_east = []
        moves_southeast = []
        moves_south = []
        moves_southwest = []
        moves_west = []
        moves_northwest = []
        
        for y in range(self.y)[::-1]:
            moves_north.append(board.get_square_from_pos((self.x, y)))
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break
            moves_northeast.append(board.get_square_from_pos((self.x + i, self.y - i)))
        for x in range(self.x + 1, 8):
            moves_east.append(board.get_square_from_pos((x, self.y)))
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_southeast.append(board.get_square_from_pos((self.x + i, self.y + i)))
        for y in range(self.y + 1, 8):
            moves_south.append(board.get_square_from_pos((self.x, y)))
        for i in range(1, 8):
            moves_southwest.append(board.get_square_from_pos((self.x - i, self.y + i)))
        for x in range(self.x)[::-1]:
            moves_west.append(board.get_square_from_pos((x, self.y)))
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_northwest.append(board.get_square_from_pos((self.x - i, self.y - i)))
        
        output.append(moves_north)
        output.append(moves_northeast)
        output.append(moves_east)
        output.append(moves_southeast)
        output.append(moves_south)
        output.append(moves_southwest)
        output.append(moves_west)
        output.append(moves_northwest)
        
        return output
            