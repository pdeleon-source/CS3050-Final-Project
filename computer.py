import random
from pieces import Piece

# this will be a class that can move pieces legally around the chess board
# Note: Doesn't have to be smart, just has to be "correct"
class Computer:
    def __init__(self, allegiance: str, board):
        self.board_array = board
        self.allegiance = allegiance

    # computer player will select a piece; returns a piece object
    def select_piece(self) -> Piece:
        available_pieces = []
        # for each square in the array representing the board
        for row in self.board_array:
            for square in row:
                # if it has a piece
                if square is not None:
                    # check if the piece is of the correct color
                    if square.allegiance == self.allegiance:
                        available_pieces.append(square)
        
        # select a random piece in the list and return it
        piece_selection = random.randrange(0, len(available_pieces))

        # print('CURRENT ROW: ', available_pieces[piece_selection].current_row)
        # print('CURRENT COL: ', available_pieces[piece_selection].current_col)
        return available_pieces[piece_selection]
    
    # computer player will move a piece
    # use select_piece() and feed it in to the piece param
    def move_piece(self, piece: Piece):
        # get the piece's moves
        possible_moves = piece.available_moves()
        # if the piece cannot move, return error code 4
        if possible_moves == []:
            return 4
        # select a random square
        random_move_square = random.randrange(0, len(possible_moves))
        # get the coords of that square
        move_coords = [possible_moves[random_move_square][0], possible_moves[random_move_square][1]]
        # move piece to square
        piece.move(move_coords)
        return 0