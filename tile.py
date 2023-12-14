import constants as c
import pygame

class Tile:
    color = None
    highlighted = False
    hovered = False
    placeable = False
    def __init__(self, position):
        self.position = position
        self.occupied = False
        self.occupied_by = None
    
    def draw_tile(self):
        current_color = c.WHITE
        if self.hovered: # mouse is hovering over tile
            current_color = c.LIGHT_GRAY
        if self.placeable: # tile can be used as a starting tile
            current_color = c.DARK_GRAY
        if self.occupied: # a piece is set here
            current_color = self.occupied_by.color
        if self.color is not None: # all other cases
            current_color = self.color
        x = self.position[0] * c.square_size + c.offside_width
        y = self.position[1] * c.square_size
        pygame.draw.rect(c.screen, c.GRAY, (x, y, c.square_size, c.square_size))
        pygame.draw.rect(c.screen, current_color, (x + c.border_size, y + c.border_size, c.square_size - 2 * c.border_size, c.square_size - 2 * c.border_size))
