import constants as c
import piece
import player
import board
import pygame

class Game:

    ALL_PIECES = []
    PLAYERS = []

    def __init__(self, pieces_shapes):
        self.pieces_shapes = pieces_shapes

        for i in range(len(c.PLAYER_COLORS)):
            CURRENT_START_POSITION = c.START_OFFSIDE_POSITIONS[i]
            self.ALL_PIECES.append([])
            rolling_y_offset = 0
            rolling_x_offset = 0
            for j in range(len(pieces_shapes)):
                current_piece = pieces_shapes[j]
                # set offside position of piece
                x = CURRENT_START_POSITION[0] + rolling_x_offset * c.square_size_offside + c.margin
                y = CURRENT_START_POSITION[1] + rolling_y_offset * c.square_size_offside + c.margin
                p = piece.Piece(current_piece, c.PLAYER_COLORS[i], [x, y])
                self.ALL_PIECES[i].append(p)
                rolling_x_offset += max([p[0] for p in current_piece]) + 2
                if rolling_x_offset >= 20:
                    rolling_y_offset += 6
                    rolling_x_offset = 0
            
            self.PLAYERS.append(player.Player(self.ALL_PIECES[i], c.PLAYER_COLORS[i], c.ALL_PLAYER_STRINGS[i]))

        
        self.board = board.Board(self.PLAYERS)
        self.board.check_if_player_has_any_placeable_pieces()

    def current_player_color(self):
        return c.ALL_PLAYER_STRINGS[self.board.current_player_index]

    def cpu_placement(self):
        if self.board.game_stop:
            self.show_winner()
        else:
            self.board.cpu_placement()

    def drawing(self):
        for players in range(len(self.ALL_PIECES)):
            for pieces in range(len(self.ALL_PIECES[players])):
                self.ALL_PIECES[players][pieces].draw_offside()
        self.board.draw_board()
        if self.board.game_stop:
            self.show_winner()
            
    def show_winner(self):
        number_of_pieces = []
        for player in range(len(self.PLAYERS)):
            pieces = self.PLAYERS[player].get_not_positioned_pieces()
            i = 0
            for piece in pieces:
                i += piece.get_piece_size()
            number_of_pieces.append(i)
        winner_index = number_of_pieces.index(min(number_of_pieces))
        pygame.display.set_caption("Blokus - Winner is Player " + self.PLAYERS[winner_index].color_text)
        '''posx, posy = (c.margin, c.margin)
        pygame.draw.rect(c.screen, c.LIGHT_GRAY_TRANSPARENT, (posx, posy / 2,150,70),0)
        font = pygame.font.SysFont('comicsans', 10)
        text = font.render('Winner is Player ' + self.current_player_color(), 1, (0,0,0))
        c.screen.blit(text, (posx + (150/2 - text.get_width()/2), posy + (70/2 - text.get_height()/2)))'''

    def mouse_event(self, mouse_pos, event):
        mouse_x, mouse_y = mouse_pos

        if self.board.game_stop:
            self.show_winner()
        else:
            # When mouse hover
            if event.type == pygame.MOUSEMOTION:
                # Check if mouse is over a piece
                for i in range(len(self.ALL_PIECES[self.board.current_player_index])):
                    self.ALL_PIECES[self.board.current_player_index][i].hover_detection(mouse_x, mouse_y)
                self.board.hover_detection(mouse_x, mouse_y)
                
            # When mouse click set piece selected
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    any_piece_selected = False
                    for i in range(len(self.ALL_PIECES[self.board.current_player_index])):
                        if self.ALL_PIECES[self.board.current_player_index][i].hovered:
                            self.ALL_PIECES[self.board.current_player_index][i].selected = True
                            any_piece_selected = True
                            self.board.clear_all_highlighted_tiles()
                            self.board.selected_piece = self.ALL_PIECES[self.board.current_player_index][i]
                        else:
                            self.ALL_PIECES[self.board.current_player_index][i].selected = False

                    
                    # if left-click on tile on board set piece
                    self.board.set_piece()
                    self.board.trigger_allowed_tiles()
                    
                if event.button == 3:
                    if self.board.hover_detection(mouse_x, mouse_y):
                        self.board.clear_all_highlighted_tiles()
                        self.board.selected_hovered_tile()
                        self.board.show_next_possible_positioning_of_selected_piece()

