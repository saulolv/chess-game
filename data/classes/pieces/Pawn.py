import pygame

from data.classes.Piece import Piece

class Pawn(Piece):
    def __init__(self, pos, color, board):
        super().__init__(pos, color, board)
        self.notation = 'Pawn'
        img_path = 'data/assets/pieces/' + self.color + '_pawn.png'
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
        
    def get_possible_moves(self, board):
        output = []
        moves = []
        
        # move forward