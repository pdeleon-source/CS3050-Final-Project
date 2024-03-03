import board

class Player:

    # base constructor
    # params: pieces (given by Board)
    #         allegiance (assigned by Board)
    #         available moves (again, from Board)
    def __init__(self, allegiance, pieces):
        self.pieces = pieces
        self.allegiance = allegiance
        # this will be moves available for a selected piece
        self.available_moves = []
        self.board = board

    # select a valid piece on the board
    # happens when a user clicks on a piece
    # params: the piece to be selected
    def SelectPiece(self, piece):
        # if the piece doesn't belong to the player, don't select
        if piece not in self.pieces:
            return
        
        # otherwise, select
        # when a piece is selected, it should show its available moves to the user
        else:
            # highlight the piece being selected
            
            # show available moves/squares somehow
            self.available_moves = self.board.get_moves(piece)
                # if the user clicks one of these available squares
                # call MovePiece on that piece with that square
            pass

    # move a selected piece to a specified square
    # this should happen after a player has selected a piece and then selected a valid square to move to
    # params: the piece to be moved, the square to move to
    def MovePiece(self, piece, row, column):
        # TODO: Again, just some filler for the time to test a bit. Not final
        piece.move(row, column)

        pass