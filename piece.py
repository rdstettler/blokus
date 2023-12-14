import constants as c
import pygame

class Piece:
    selected = False
    positioned = False
    hovered = False
    placeable = True # All pieces ar initialy placeable except the x-piece
    
    def __init__(self, piece, color, offside_position = [0,0]):
        self.piece = piece
        self.color = color
        self.variations = self.piece_variations()
        self.offside_position = offside_position
        if self.piece == [[0,0],[1,0],[-1,0],[0,1],[0,1]]:
            self.placeable = False
        
    def get_piece_size(self):
        return len(self.piece)
    
    def get_position_of_tile_offside(self, tile):
        isXPiece = 0
        if self.piece == [[0,0],[1,0],[-1,0],[0,1],[0,1]]:
            isXPiece = 1
        x0,y0 = self.offside_position[0], self.offside_position[1]
        return [x0 + (tile[0] + isXPiece) * c.square_size_offside, y0 + (tile[1] + isXPiece) * c.square_size_offside]
    
    def hover_detection(self, mouse_x, mouse_y):
        self.hovered = False
        if self.positioned or not self.placeable:
            return False
        for p in range(len(self.piece)):
            x, y = self.get_position_of_tile_offside(self.piece[p])
            if mouse_x >= x and mouse_x <= x + c.square_size_offside and mouse_y >= y and mouse_y <= y + c.square_size_offside:
                self.hovered = True
        self.draw_offside()
        
    def draw_offside(self):
        drawing_color = self.color
        border = 0
        lightened_color = tuple([int(c * 0.7) for c in self.color])
        if self.hovered:
            drawing_color = lightened_color
        if self.selected:
            border = 1
        if self.positioned:
            drawing_color = c.LIGHT_GRAY
        if not self.placeable and not self.positioned:
            drawing_color = lightened_color
        for p in range(len(self.piece)):
            x, y = self.get_position_of_tile_offside(self.piece[p])
            pygame.draw.rect(c.screen, drawing_color, (x, y, c.square_size_offside, c.square_size_offside), border)

    def piece_variations(self):
        # define tuple
        variations = []
        # add original item to tuple
        for p in range(len(self.piece)):
            new_center_tile = [self.piece[p][0] - self.piece[0][0], self.piece[p][1] - self.piece[0][1]]
            # move all tiles in piece such, that new_center_tile is at [0,0]
            new_piece = [[x - new_center_tile[0], y - new_center_tile[1]] for x, y in self.piece]
            variations.append(new_piece)
            for i in range(3):
                new_piece = self.rotate_90degrees(new_piece)
                variations.append(new_piece)
            mirrored_piece = self.mirror_piece(new_piece)
            for i in range(4):
                mirrored_piece = self.rotate_90degrees(mirrored_piece)
                variations.append(mirrored_piece)
        tuple_lists = [tuple(map(tuple, mylist)) for mylist in variations]
        # Add the tuples to a set to remove duplicates
        unique_tuple_lists = set(tuple_lists)
        # Convert the unique tuples back to lists
        uniques = [list(map(list, mylist)) for mylist in unique_tuple_lists]
        return uniques    
    
    def rotate_90degrees(self, piece):
        # rotate piece 90 degrees
        rotated_piece = []
        for i in range(len(piece)):
            rotated_piece.append([piece[i][1], -piece[i][0]])
        return rotated_piece

    def mirror_piece(self, piece):
        # mirror piece
        mirrored_piece = []
        for i in range(len(piece)):
            mirrored_piece.append([piece[i][0], -piece[i][1]])
        return mirrored_piece