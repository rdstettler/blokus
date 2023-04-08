import pygame
import sys
import random

# Initialisierung von pygame
pygame.init()

# Fenstergröße und -titel
board_size = 21
border_size = 1
square_size = 20
square_size_offside = square_size * 0.5
offside_width = 250
margin = 5
size = (square_size * board_size + 2 * offside_width, square_size * board_size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Blokus")
SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()
# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (240, 240, 240)
GAME_FONT = pygame.font.SysFont("Comic Sans MS", 24)
LIGHT_RED = (255, 100, 100)
LIGHT_BLUE = (100, 100, 255)
LIGHT_YELLOW = (255, 255, 100)
LIGHT_GREEN = (100, 255, 100)
PLAYER_COLORS = [RED, GREEN, BLUE, YELLOW]
LIGHT_COLORS = [LIGHT_RED, LIGHT_GREEN, LIGHT_BLUE, LIGHT_YELLOW]

RED_OFFSIDE_START = [0,0]
GREEN_OFFSIDE_START = [0, size[1] / 2]
BLUE_OFFSIDE_START = [offside_width + square_size * board_size, size[1] / 2]
YELLOW_OFFSIDE_START = [offside_width + square_size * board_size, 0]
START_OFFSIDE_POSITIONS = [RED_OFFSIDE_START, GREEN_OFFSIDE_START, BLUE_OFFSIDE_START, YELLOW_OFFSIDE_START]
ALL_PLAYER_STRINGS = ["RED", "GREEN", "BLUE", "YELLOW"]

RED_START = [0,0]
GREEN_START = [0, board_size - 1]
BLUE_START = [board_size - 1, board_size - 1]
YELLOW_START = [board_size - 1, 0]
START_POSITIONS = [RED_START, GREEN_START, BLUE_START, YELLOW_START]

RED_PIECES = []
GREEN_PIECES = []
BLUE_PIECES = []
YELLOW_PIECES = []
ALL_PIECES = [RED_PIECES, GREEN_PIECES, BLUE_PIECES, YELLOW_PIECES]

# Set screen background color
screen.fill(GRAY)

# Define player pieces_shapes as collection of arrays
pieces_shapes = (
    [[0,0]],
    [[0,0],[0,1]],
    [[0,0],[0,1],[0,2]],
    [[0,0],[0,1],[0,2],[0,3]],
    [[0,0],[0,1],[0,2],[0,3],[0,4]],
    [[0,0],[0,1],[1,0]], # small L
    [[0,0],[0,1],[0,2],[1,0]], # L
    [[0,0],[1,0],[0,1],[1,1]], # Square
    [[0,0],[1,0],[1,1],[2,1]], # S-piece
    [[0,0],[1,0],[2,0],[1,1]], # small T-piece
    [[0,0],[0,1],[0,2],[0,3],[1,0]], # big L
    [[0,0],[1,0],[0,1],[1,1],[0,2]], # Square with nibble
    
    [[0,0],[1,0],[2,0],[1,1],[1,2]], # T-piece
    [[0,0],[1,0],[1,1],[1,2],[2,2]], # Z-piece
    [[0,0],[1,0],[0,1],[0,2],[1,2]], # C-piece
    [[0,0],[1,1],[1,0],[2,0],[3,0]], # F-piece
    [[0,0],[1,0],[1,1],[2,1],[2,2]], # W-piece
    [[0,0],[1,0],[1,1],[1,2],[2,1]],
    [[0,0],[1,0],[-1,0],[0,1],[0,1]] # X-Piece
)

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
        current_color = WHITE
        if self.hovered: # mouse is hovering over tile
            current_color = LIGHT_GRAY
        if self.placeable: # tile can be used as a starting tile
            current_color = DARK_GRAY
        if self.occupied: # a piece is set here
            current_color = self.occupied_by.color
        if self.color is not None: # all other cases
            current_color = self.color
        x = self.position[0] * square_size + offside_width
        y = self.position[1] * square_size
        pygame.draw.rect(screen, GRAY, (x, y, square_size, square_size))
        pygame.draw.rect(screen, current_color, (x + border_size, y + border_size, square_size - 2 * border_size, square_size - 2 * border_size))


class Board:
    tiles = [] # 2D array of tiles
    selected_piece = None
    hovered_tile = None
    current_variation_index = None
    current_player_index = 0
    selected_tile = None
    selected_piece_index = None
    def __init__(self, players):
        self.Players = players
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(Tile([i,j]))
            self.tiles.append(row)
    
    def draw_board(self):
        # call draw function of each tile
        for t in self.tiles:
            for r in t:
                r.draw_tile()
    
    def hover_detection(self, mouse_x, mouse_y):
        hovering = False
        for i in range(board_size):
            for j in range(board_size):
                x = self.tiles[i][j].position[0] * square_size + offside_width
                y = self.tiles[i][j].position[1] * square_size
                self.tiles[i][j].hovered = False
                if mouse_x > x and mouse_x < x + square_size and mouse_y > y and mouse_y < y + square_size:
                    self.hovered_tile = self.tiles[i][j]
                    self.hovered_tile.hovered = True
                    if self.hovered_tile.placeable:
                        hovering = True
        if not hovering:
            self.hovered_tile = None
        return hovering
    
    def cpu_placement(self):
        # computer places a piece
        self.check_if_player_has_any_placeable_pieces()
        placeable_pieces = self.Players[self.current_player_index].get_placeable_pieces()
        # sort placeable pieces by size descending and select the largest one
        self.selected_piece = sorted(placeable_pieces, key=lambda piece: piece.get_piece_size(), reverse=True)[0]
        # filter placeable pieces by size and get only the largest ones, then select randomly from them
        largest_pieces = [piece for piece in placeable_pieces if piece.get_piece_size() == self.selected_piece.get_piece_size()]
        self.selected_piece = random.choice(largest_pieces)
        
        self.trigger_allowed_tiles()
        allowed_tiles = []
        for i in range(board_size):
            for j in range(board_size):
                if self.tiles[i][j].placeable:
                    allowed_tiles.append(self.tiles[i][j])
        random_tile_index = random.randint(0, len(allowed_tiles) - 1)
        self.selected_tile = allowed_tiles[random_tile_index]
        
        variation = self.get_next_possible_variation()
        # highlight all tiles (can probably be done more elegantly)
        for i in range(len(variation)):
            x,y = variation[i]
            self.tiles[x + self.selected_tile.position[0]][y + self.selected_tile.position[1]].highlighted = True
        self.set_piece(cpu_move=True)
        

    def selected_hovered_tile(self):
        self.selected_tile = self.hovered_tile
    
    def clear_all_highlighted_tiles(self):
        for i in range(board_size):
            for j in range(board_size):
                self.tiles[i][j].highlighted = None
                self.tiles[i][j].color = None
                
    def show_next_possible_positioning_of_selected_piece(self):
        if self.selected_piece != None:
            variation = self.get_next_possible_variation()
            if variation != None:
                for i in range(len(variation)):
                    x,y = variation[i]
                    self.tiles[x + self.selected_tile.position[0]][y + self.selected_tile.position[1]].color = LIGHT_COLORS[self.current_player_index]
                    self.tiles[x + self.selected_tile.position[0]][y + self.selected_tile.position[1]].highlighted = True
                
    def set_piece(self, cpu_move = False):
        if self.hovered_tile is not None or cpu_move:
            if self.selected_piece is not None:
                self.selected_piece.positioned = True
                self.selected_piece.draw_offside()
                self.selected_piece = None
            for i in range(board_size):
                for j in range(board_size):
                    current_tile = self.tiles[i][j]
                    if current_tile.highlighted:
                        current_tile.highlighted = False
                        current_tile.placeable = False
                        current_tile.occupied = True
                        current_tile.occupied_by = self.Players[self.current_player_index]
                        current_tile.color = PLAYER_COLORS[self.current_player_index]
                        current_tile.draw_tile()
            self.clear_all_highlighted_tiles()
            self.Players[self.current_player_index].has_placed_piece = True
            self.Players[self.current_player_index].positioned_pieces += 1
            self.Players[self.current_player_index].is_current_player = False
            
            current_player_index = self.current_player_index
            has_placeable_pieces = False
            while not has_placeable_pieces:
                self.current_player_index = (self.current_player_index + 1) % 4
                self.Players[self.current_player_index].is_current_player = True
                has_placeable_pieces = self.check_if_player_has_any_placeable_pieces()
                if not has_placeable_pieces:
                    self.Players[self.current_player_index].playing = False
                    self.Players[self.current_player_index].loser = True
                if self.current_player_index == current_player_index:
                    break
                
            if self.current_player_index == current_player_index:
                # declare winner
                self.Players[self.current_player_index].winner = True
    
    def check_if_player_has_any_placeable_pieces(self):
        for piece in self.Players[self.current_player_index].pieces:
            piece.placeable = False
        not_positioned_pieces_from_player = self.Players[self.current_player_index].get_not_positioned_pieces()
        for i in range(len(not_positioned_pieces_from_player)):
            piece_is_placeable = self.check_if_piece_is_placeable(not_positioned_pieces_from_player[i])
            if piece_is_placeable:
                not_positioned_pieces_from_player[i].placeable = True
        if any(x.placeable == True for x in not_positioned_pieces_from_player):
            return True
        
        return False
    
    def check_if_piece_is_placeable(self, piece):
        for variation in piece.variations:
            for i in range(board_size):
                for j in range(board_size):
                    tile = self.tiles[i][j]
                    check_if_tile_is_placeable = self.tile_placeable_by_player(tile.position)
                    # if player has no pieces played, set only starting tile
                    if self.Players[self.current_player_index].positioned_pieces == 0:
                        x0,y0 = START_POSITIONS[self.current_player_index]
                        if tile.position[0] == x0 and tile.position[1] == y0:
                            check_if_tile_is_placeable = True
                    if check_if_tile_is_placeable:
                        placeable = self.check_placeability_of_variation(variation, tile)
                        if placeable:
                            return True
        return False
    
    def get_next_possible_variation(self):
        if self.selected_piece != None:
            if self.current_variation_index == None:
                self.current_variation_index = -1
            i = 0
            while i < len(self.selected_piece.variations):
                self.current_variation_index = (self.current_variation_index + 1) % len(self.selected_piece.variations)
                variation = self.selected_piece.variations[self.current_variation_index]
                if self.check_placeability_of_variation(variation, self.selected_tile):
                    return variation
                else:
                    i += 1
            
    def check_placeability_of_variation(self, variation, tile):
        for i in range(len(variation)):
            piece_tile = variation[i]
            x,y = piece_tile
            placeable = self.tile_placeable_by_player([x + tile.position[0], y + tile.position[1]])
            if placeable is False:
                return False
        return True
    
    def tile_placeable_by_player(self, tile_cooridates):
        i,j = tile_cooridates
        if i >= board_size or i < 0 or j >= board_size or j < 0:
            return False
        if self.tiles[i][j].occupied:
            return False
        top_left_tile = None
        top_right_tile = None
        bottom_left_tile = None
        bottom_right_tile = None
        top_tile = None
        left_tile = None
        right_tile = None
        bottom_tile = None
        if i > 0:
            left_tile = self.tiles[i-1][j]
            if j > 0:
                bottom_left_tile = self.tiles[i-1][j-1]
            if j < board_size - 1:
                top_left_tile = self.tiles[i-1][j+1]
        if i < board_size - 1:
            right_tile = self.tiles[i+1][j]
            if j > 0:
                bottom_right_tile = self.tiles[i+1][j-1]
            if j < board_size - 1:
                top_right_tile = self.tiles[i+1][j+1]
        if j > 0:
            bottom_tile = self.tiles[i][j-1]
        if j < board_size - 1:
            top_tile = self.tiles[i][j+1]
        if (top_tile != None and top_tile.occupied_by is not None and top_tile.occupied_by.is_current_player) or \
            (left_tile != None and left_tile.occupied_by is not None and left_tile.occupied_by.is_current_player) or \
            (right_tile != None and right_tile.occupied_by is not None and right_tile.occupied_by.is_current_player) or \
            (bottom_tile != None and bottom_tile.occupied_by is not None and bottom_tile.occupied_by.is_current_player):
            return False
        else:
            if (top_left_tile != None and top_left_tile.occupied_by is not None and top_left_tile.occupied_by.is_current_player) or \
                (top_right_tile != None and top_right_tile.occupied_by is not None and top_right_tile.occupied_by.is_current_player) or \
                (bottom_left_tile != None and bottom_left_tile.occupied_by is not None and bottom_left_tile.occupied_by.is_current_player) or \
                (bottom_right_tile != None and bottom_right_tile.occupied_by is not None and bottom_right_tile.occupied_by.is_current_player):
                return True
            else:
                return None
                
    
    def trigger_allowed_tiles(self):
        if self.Players[self.current_player_index].positioned_pieces == 0:
            x0,y0 = START_POSITIONS[self.current_player_index]
            self.tiles[int(x0)][int(y0)].placeable = True
            self.tiles[int(x0)][int(y0)].draw_tile()
            for i in range(board_size):
                for j in range(board_size):
                    if i is not x0 and j is not y0:
                        self.tiles[i][j].placeable = False
                        self.tiles[i][j].draw_tile()
        else:
            for i in range(board_size):
                for j in range(board_size):
                    placeability = self.tile_placeable_by_player([i,j])
                    if placeability and self.selected_piece is not None:
                        placeability = False
                        for variation in self.selected_piece.variations:
                            if self.check_placeability_of_variation(variation, self.tiles[i][j]):
                                placeability = True
                                break
                    if placeability:
                        self.tiles[i][j].placeable = True
                        self.tiles[i][j].draw_tile()
                    else:
                        self.tiles[i][j].placeable = False
                        self.tiles[i][j].draw_tile()

class Player:
    is_current_player = False
    playing = True
    winner = False
    loser = False
    positioned_pieces = 0
    def __init__(self, pieces, color, color_text):
        self.color = color
        self.pieces = pieces
        self.color_text = color_text

    def get_not_positioned_pieces(self):
        not_positioned_pieces = []
        for piece in self.pieces:
            if piece.positioned is False:
                not_positioned_pieces.append(piece)
        return not_positioned_pieces
    
    def get_placeable_pieces(self):
        placeable_pieces = []
        for piece in self.pieces:
            if piece.placeable and piece.positioned is False:
                placeable_pieces.append(piece)
        return placeable_pieces

class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 10)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

class Piece:
    selected = False
    positioned = False
    hovered = False
    placeable = False
    
    def __init__(self, piece, color, offside_position = [0,0]):
        self.piece = piece
        self.color = color
        self.variations = self.piece_variations()
        self.offside_position = offside_position
        
    def get_piece_size(self):
        return len(self.piece)
        
    def get_not_positioned_pieces(self):
        not_positioned_pieces = []
        for p in self.pieces:
            if not p.positioned:
                not_positioned_pieces.append(p)
        return not_positioned_pieces
    
    def get_position_of_tile(self, tile):
        x0,y0 = self.offside_position[0], self.offside_position[1]
        return [x0 + tile[0] * square_size_offside, y0 + tile[1] * square_size_offside]
    
    def hover_detection(self, mouse_x, mouse_y):
        if self.positioned or not self.placeable:
            return False
        self.hovered = False
        for p in range(len(self.piece)):
            x, y = self.get_position_of_tile(self.piece[p])
            if mouse_x >= x and mouse_x <= x + square_size_offside and mouse_y >= y and mouse_y <= y + square_size_offside:
                self.hovered = True
        self.draw_offside()
        
    def draw_offside(self):
        drawing_color = self.color
        border = 0
        if self.hovered:
            lightened_color = tuple([int(c * 0.7) for c in self.color])
            drawing_color = lightened_color
        if self.selected:
            border = 1
        if self.positioned:
            drawing_color = LIGHT_GRAY
        if not self.placeable:
            drawing_color = DARK_GRAY
        for p in range(len(self.piece)):
            x, y = self.get_position_of_tile(self.piece[p])
            pygame.draw.rect(screen, drawing_color, (x, y, square_size_offside, square_size_offside), border)
                              
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
                new_piece = rotate_90degrees(new_piece)
                variations.append(new_piece)
            mirrored_piece = mirror_piece(new_piece)
            for i in range(4):
                mirrored_piece = rotate_90degrees(mirrored_piece)
                variations.append(mirrored_piece)
        tuple_lists = [tuple(map(tuple, mylist)) for mylist in variations]
        # Add the tuples to a set to remove duplicates
        unique_tuple_lists = set(tuple_lists)
        # Convert the unique tuples back to lists
        uniques = [list(map(list, mylist)) for mylist in unique_tuple_lists]
        return uniques    
    
def rotate_90degrees(piece):
    # rotate piece 90 degrees
    rotated_piece = []
    for i in range(len(piece)):
        rotated_piece.append([piece[i][1], -piece[i][0]])
    return rotated_piece

def mirror_piece(piece):
    # mirror piece
    mirrored_piece = []
    for i in range(len(piece)):
        mirrored_piece.append([piece[i][0], -piece[i][1]])
    return mirrored_piece

PLAYERS = []

def draw_stuff():
    for c in range(len(PLAYER_COLORS)):
        CURRENT_START_POSITION = START_OFFSIDE_POSITIONS[c]
            
        rolling_y_offset = 0
        rolling_x_offset = 0
        for i in range(len(pieces_shapes)):
            current_piece = pieces_shapes[i]
            # draw current_piece
            x = CURRENT_START_POSITION[0] + rolling_x_offset * square_size_offside + margin
            y = CURRENT_START_POSITION[1] + rolling_y_offset * square_size_offside + margin
            p = Piece(current_piece, PLAYER_COLORS[c], [x, y])
            ALL_PIECES[c].append(p)
            p.draw_offside()

            rolling_x_offset += max([p[0] for p in current_piece]) + 2
            if rolling_x_offset >= 20:
                rolling_y_offset += 6
                rolling_x_offset = 0
        
        PLAYERS.append(Player(ALL_PIECES[c], PLAYER_COLORS[c], ALL_PLAYER_STRINGS[c]))

BOARD = Board(PLAYERS)
BOARD.draw_board()

any_piece_selected = False
draw_stuff()
# add button that triggers computer to play
button = Button(LIGHT_GRAY, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 30, 90, 30, "Computer")
button.draw(screen)
# Spielschleife
running = True
while running:    
    for event in pygame.event.get():
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        # When mouse hover
        if event.type == pygame.MOUSEMOTION:
            # Check if mouse is over a piece
        
            for i in range(len(ALL_PIECES[BOARD.current_player_index])):
                ALL_PIECES[BOARD.current_player_index][i].hover_detection(mouse_x, mouse_y)
            
            BOARD.hover_detection(mouse_x, mouse_y)
            
        # When mouse click set piece selected
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                any_piece_selected = False
                for i in range(len(ALL_PIECES[BOARD.current_player_index])):
                    if ALL_PIECES[BOARD.current_player_index][i].hovered:
                        ALL_PIECES[BOARD.current_player_index][i].selected = True
                        any_piece_selected = True
                        BOARD.clear_all_highlighted_tiles()
                        BOARD.selected_piece = ALL_PIECES[BOARD.current_player_index][i]
                    else:
                        ALL_PIECES[BOARD.current_player_index][i].selected = False

                
                # if left-click on tile on board set piece
                BOARD.set_piece()
                
                if button.isOver([mouse_x, mouse_y]):
                    BOARD.cpu_placement()
                
            if event.button == 3:
                if BOARD.hover_detection(mouse_x, mouse_y):
                    BOARD.clear_all_highlighted_tiles()
                    BOARD.selected_hovered_tile()
                    BOARD.show_next_possible_positioning_of_selected_piece()
                    BOARD.draw_board()

    # if any piece selected, highlight all possible positions in the game board
    if any_piece_selected:
        BOARD.trigger_allowed_tiles()
    else:
        BOARD.selected_piece = None
        BOARD.check_if_player_has_any_placeable_pieces()
        BOARD.draw_board()
    
    # Add colored Circle at the bottom left of the screen indicating the current player
    pygame.draw.circle(screen, PLAYER_COLORS[BOARD.current_player_index], (square_size_offside, size[1] - square_size_offside), square_size_offside)
    
    # Aktualisiere das Display
    pygame.display.flip()

# Beende das Programm
pygame.quit()
sys.exit()
