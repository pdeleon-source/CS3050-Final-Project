class Player:

    # base constructor
    # params: allegience (assigned by Board)
    #         pieces (given by Board)
    #         available moves (again, from Board)
    def __init__(self, allegience, pieces, available_moves):
        self.pieces = pieces
        self.allegience = allegience
        self.available_moves = available_moves

    # select a valid piece on the board
    # params: the piece to be selected
    def SelectPiece(self, piece):
        # if the piece and player allegience don't match, don't select
        if piece.allegience != self.allegience:
            return
        # otherwise, select
        # Not sure what to do for this right now, have this as filler
        # TODO: Update this
        else:
            piece.selected = True

    # move a selected piece to a specified square
    # params: the piece to be moved, the square to move to
    def MovePiece(self, piece, square):
        # TODO: Again, just some filler for the time to test a bit. Not final
        piece.location = square
        # TODO: After moving the piece, need to update the board appropriately
        # Remove piece from old location, and add it to new location
        pass