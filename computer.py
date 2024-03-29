import random
from pieces import Piece
import numpy as np

SQUARE_WIDTH = 400 // 8
SQUARE_HEIGHT = 400 // 8


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
        valid_move = False
        move_coords = []
        while not valid_move:

            # get the piece's moves
            possible_moves, possible_captures = piece.available_moves()

            all_moves = possible_moves + possible_captures
            # if the piece cannot move, return error code 4
            if all_moves == []:
                return 4
            # select a random square
            random_move_square = random.randrange(0, len(all_moves))
            # get the coords of that square
            # print(all_moves)
            # print("MOVE SQUARE: ", all_moves[random_move_square])
            move_coords = [all_moves[random_move_square][0], all_moves[random_move_square][1]]
            # move piece to square

            # Store the piece's current position
            current_row = piece.current_row
            current_col = piece.current_col

            # Move piece to square
            print(f"Piece: {piece}")

            valid_move = piece.move(move_coords)

            # Update the piece's position in the board_array
            if valid_move:
                print(f"moved {self} from [{current_row} {current_col}]")
                # print(f"Current Piece removal: {move_coords[1]]")
                self.board_array[current_row][current_col] = None
                self.board_array[move_coords[0]][move_coords[1]] = piece

        return move_coords