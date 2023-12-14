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

    def reset_all_pieces(self):
        for piece in self.pieces:
            piece.placeable = False