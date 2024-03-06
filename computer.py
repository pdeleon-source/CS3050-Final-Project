import random
from pieces import Piece

# this will be a class that can move pieces legally around the chess board
# Note: Doesn't have to be smart, just has to be "correct"
class Computer:
    def __init__(self, allegiance, board):
        self.board_object = board
        self.allegiance = allegiance

    # computer player will select a piece; returns a piece object
    def select_piece(self) -> Piece:
        available_pieces = []
        # for each square in the array representing the board
        for square in self.board.board:
            # if it has a piece
            if square is not None:
                # check if the piece is of the correct color
                if square.allegiance == self.allegiance:
                    available_pieces.append(square)
        
        # select a random piece in the list and return it
        piece_selection = random.randrange(0, len(available_pieces))
        return available_pieces[piece_selection]
    
    # computer player will move a piece
    # use select_piece() and feed it in to the piece param
    def move_piece(self, piece: Piece):
        # get the piece's moves
        possible_moves = piece.available_moves()
        # select a random square
        random_move_square = random.randrange(0, len(possible_moves))
        # get the coords of that square
        move_coords = [random_move_square[0], random_move_square[1]]
        # move piece to square
        piece.move(move_coords)