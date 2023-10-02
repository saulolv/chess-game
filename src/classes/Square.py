import pygame

class Square:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.abs_x = x * width
        self.abs_y = y * height
        self.abs_pos = (self.abs_x, self.abs_y)
        self.pos = (self.x, self.y)
        self.color = 'lightgray' if (self.x + self.y) % 2 == 0 else 'darkgray'
        self.draw_color = (220, 208, 194) if self.color == 'lightgray' else (100, 100, 100)
        self.highlight_color = (100, 249, 83) if self.color == 'lightgray' else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        self.rect = pygame.Rect(self.abs_x, self.abs_y, self.width, self.height)
        
    # get the formal notation of the tile
    def get_coord(self):
        columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return columns[self.x] + str(self.y + 1)
    
    def draw(self, screen):
        # configures if tle should be light or dark or highlighted
        if self.highlight:
            pygame.draw.rect(screen, self.highlight_color, self.rect)
        else:
            pygame.draw.rect(screen, self.draw_color, self.rect)
        
        # adds the chess piece icons
        if self.occupying_piece:
            centering_rect = self.occupying_piece.img.get_rect(center=self.rect.center)
            centering_rect.center = (centering_rect.center[0] + 1, centering_rect.center[1] + 1)
            screen.blit(self.occupying_piece.img, centering_rect)
            