class Player:

    # base constructor
    # params: allegiance (assigned by Board)
    #         pieces (given by Board)
    #         available moves (again, from Board)
    def __init__(self, allegiance, pieces, available_moves):
        self.pieces = pieces
        self.allegiance = allegiance
        self.available_moves = available_moves

    # select a valid piece on the board
    # params: the piece to be selected
    def SelectPiece(self, piece):
        # if the piece and player allegience don't match, don't select
        if piece.allegiance != self.allegiance:
            return
        # otherwise, select
        # Not sure what to do for this right now, have this as filler
        # TODO: Update this
        else:
            piece.selected = True

    # move a selected piece to a specified square
    # params: the piece to be moved, the square to move to
    def MovePiece(self, piece, row, column):
        # TODO: Again, just some filler for the time to test a bit. Not final
        piece.move(row, column)

        pass