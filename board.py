import constants as c
import random
import tile

class Board:
    tiles = [] # 2D array of tiles
    selected_piece = None
    hovered_tile = None
    current_variation_index = None
    Player = None
    Players = []
    selected_tile = None
    selected_piece_index = None
    current_player_index = 0
    game_stop = False
    def __init__(self, players):
        self.Players = players
        self.Player = self.Players[0]
        for i in range(c.board_size):
            row = []
            for j in range(c.board_size):
                row.append(tile.Tile([i,j]))
            self.tiles.append(row)
    
    def draw_board(self):
        # call draw function of each tile
        for t in self.tiles:
            for r in t:
                r.draw_tile()
    
    def hover_detection(self, mouse_x, mouse_y):
        hovering = False
        for i in range(c.board_size):
            for j in range(c.board_size):
                x = self.tiles[i][j].position[0] * c.square_size + c.offside_width
                y = self.tiles[i][j].position[1] * c.square_size
                self.tiles[i][j].hovered = False
                if mouse_x > x and mouse_x < x + c.square_size and mouse_y > y and mouse_y < y + c.square_size:
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
        placeable_pieces = self.Player.get_placeable_pieces()
        # sort placeable pieces by size descending and select the largest one
        self.selected_piece = sorted(placeable_pieces, key=lambda piece: piece.get_piece_size(), reverse=True)[0]
        # filter placeable pieces by size and get only the largest ones, then select randomly from them
        largest_pieces = [piece for piece in placeable_pieces if piece.get_piece_size() == self.selected_piece.get_piece_size()]
        self.selected_piece = random.choice(largest_pieces)
        
        self.trigger_allowed_tiles()
        allowed_tiles = []
        for i in range(c.board_size):
            for j in range(c.board_size):
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
        for i in range(c.board_size):
            for j in range(c.board_size):
                self.tiles[i][j].highlighted = None
                self.tiles[i][j].color = None
                
    def show_next_possible_positioning_of_selected_piece(self):
        if self.selected_piece != None:
            variation = self.get_next_possible_variation()
            if variation != None:
                for i in range(len(variation)):
                    x,y = variation[i]
                    self.tiles[x + self.selected_tile.position[0]][y + self.selected_tile.position[1]].color = c.LIGHT_COLORS[self.current_player_index]
                    self.tiles[x + self.selected_tile.position[0]][y + self.selected_tile.position[1]].highlighted = True
                
    def set_piece(self, cpu_move = False):
        if (self.hovered_tile is not None and self.hovered_tile == self.selected_tile) or cpu_move:
            if self.selected_piece is not None:
                self.selected_piece.positioned = True
                self.selected_piece.draw_offside()
                self.selected_piece = None
            for i in range(c.board_size):
                for j in range(c.board_size):
                    current_tile = self.tiles[i][j]
                    if current_tile.highlighted:
                        current_tile.highlighted = False
                        current_tile.placeable = False
                        current_tile.occupied = True
                        current_tile.occupied_by = self.Player
                        current_tile.color = self.Player.color
                        current_tile.draw_tile()
            self.clear_all_highlighted_tiles()
            self.Player.has_placed_piece = True
            self.Player.positioned_pieces += 1
            self.Player.is_current_player = False
            self.next_player()
            
    
    def next_player(self):
        has_placeable_pieces = False
        current_player_index = self.current_player_index
        i = 0
        while not has_placeable_pieces and i < 5:
            self.Players[self.current_player_index].is_current_player = False
            self.current_player_index = (self.current_player_index + 1) % 4
            self.Players[self.current_player_index].is_current_player = True
            has_placeable_pieces = self.check_if_player_has_any_placeable_pieces()
            if not has_placeable_pieces:
                self.Players[self.current_player_index].playing = False
                self.Players[self.current_player_index].loser = True
            i += 1
        
        if has_placeable_pieces:
            self.Player = self.Players[self.current_player_index]
        else: # no more players can set pieces
            self.game_stop = True
            

    def check_if_player_has_any_placeable_pieces(self):
        self.Players[self.current_player_index].reset_all_pieces()
        not_positioned_pieces_from_player = self.Players[self.current_player_index].get_not_positioned_pieces()
        for i in range(len(not_positioned_pieces_from_player)):
            piece_is_placeable = self.check_if_piece_is_placeable(not_positioned_pieces_from_player[i])
            if piece_is_placeable:
                not_positioned_pieces_from_player[i].placeable = True
            else:
                not_positioned_pieces_from_player[i].placeable = False
        if any(x.placeable == True for x in not_positioned_pieces_from_player):
            return True
        return False
    
    def check_if_piece_is_placeable(self, piece):
        for i in range(c.board_size):
            for j in range(c.board_size):
                tile = self.tiles[i][j]
                if not tile.occupied:
                    for variation in piece.variations:
                        check_if_tile_is_placeable = self.tile_placeable_by_player(tile.position)
                        # if player has no pieces played, set only starting tile
                        if self.Players[self.current_player_index].positioned_pieces == 0:
                            x0,y0 = c.START_POSITIONS[self.current_player_index]
                            if tile.position[0] == x0 and tile.position[1] == y0:
                                check_if_tile_is_placeable = True
                        if check_if_tile_is_placeable:
                            placeable = self.check_placeability_of_variation(variation, tile)
                            if placeable:
                                return True
        return False
    
    def get_next_possible_variation(self):
        if self.selected_piece != None and self.selected_tile != None:
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
        if i >= c.board_size or i < 0 or j >= c.board_size or j < 0:
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
            if j < c.board_size - 1:
                top_left_tile = self.tiles[i-1][j+1]
        if i < c.board_size - 1:
            right_tile = self.tiles[i+1][j]
            if j > 0:
                bottom_right_tile = self.tiles[i+1][j-1]
            if j < c.board_size - 1:
                top_right_tile = self.tiles[i+1][j+1]
        if j > 0:
            bottom_tile = self.tiles[i][j-1]
        if j < c.board_size - 1:
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
        # At the start of the game, only corner is allowed
        if self.Players[self.current_player_index].positioned_pieces == 0:
            x0,y0 = c.START_POSITIONS[self.current_player_index]
            self.tiles[int(x0)][int(y0)].placeable = True
            self.tiles[int(x0)][int(y0)].draw_tile()
            for i in range(c.board_size):
                for j in range(c.board_size):
                    if i is not x0 and j is not y0:
                        self.tiles[i][j].placeable = False
                        self.tiles[i][j].draw_tile()
        else:
            for i in range(c.board_size):
                for j in range(c.board_size):
                    placeability = self.tile_placeable_by_player([i,j])
                    if placeability is True and self.selected_piece is not None:
                        placeability = False
                        for variation in self.selected_piece.variations:
                            if self.check_placeability_of_variation(variation, self.tiles[i][j]):
                                placeability = True
                                break
                    if placeability:
                        self.tiles[i][j].placeable = True
                    else:
                        self.tiles[i][j].placeable = False
                    self.tiles[i][j].draw_tile()
