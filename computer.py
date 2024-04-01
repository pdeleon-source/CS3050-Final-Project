import random
from pieces import Piece
import pieces as p
import numpy as np

SQUARE_WIDTH = 400 // 8
SQUARE_HEIGHT = 400 // 8


# this will be a class that can move pieces legally around the chess board
# Note: Doesn't have to be smart, just has to be "correct"
class Computer:
    def __init__(self, allegiance: str, board):
        self.board_array = board

        self.allegiance = allegiance
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # self.make_demo_board()

    # computer player will select a piece; returns a piece object
    def select_piece(self):
        available_pieces = []
        # for each square in the array representing the board
        for row in self.board_array:
            for square in row:
                # if it has a piece
                if square is not None:
                    # check if the piece is of the correct color
                    if square.allegiance == self.allegiance:
                        available_pieces.append(square)

        return available_pieces

    def select_random_piece(self, available_pieces):

        # select a random piece in the list and return it
        piece_location = random.randrange(0, len(available_pieces))
        piece_selection = available_pieces[piece_location]

        all_moves = []

        while all_moves == []:
            piece_location = random.randrange(0, len(available_pieces))
            piece_selection = available_pieces[piece_location]
            possible_moves, possible_captures, attacks = piece_selection.available_moves()
            all_moves = possible_moves + possible_captures

        # select a random square
        random_move_square = random.randrange(0, len(all_moves))

        # get the coords of that square
        move_coords = [all_moves[random_move_square][0], all_moves[random_move_square][1]]

        return piece_selection, move_coords
    
    # computer player will move a piece
    # use select_piece() and feed it in to the piece param
    def move_piece(self, piece: Piece, move_coords):

        # Store the piece's current position
        current_row = piece.current_row
        current_col = piece.current_col

        # Move piece to square
        print(f"Piece: {piece}")

        valid_move = piece.move(move_coords)

        # Update the piece's position in the board_array
        if valid_move:
            print(f"moved {self} from [{current_row} {current_col}]")
            self.board_array[current_row][current_col] = None
            self.board_array[move_coords[0]][move_coords[1]] = piece

    def evaluate(self):
        max_value = 0
        best_move = None
        available_pieces = self.select_piece()
        for piece in available_pieces:
            # Get all possible moves for this piece
            possible_moves, possible_captures, attacks = piece.available_moves()
            # print("=====++++++++++++++=====")
            # print(f"CurrPiece: {piece})")

            for move in possible_moves + possible_captures:
                # Calculate the value of the move (for simplicity, assume captured piece's value is 1)
                target_row, target_col = move
                target_piece = self.board_array[target_row][target_col]
                move_value = target_piece.get_value() if target_piece is not None else 0

                # print(f"Target: {target_piece}, Value: {move_value}")

                if move_value > max_value:
                     max_value = move_value
                     best_move = (piece, move)

            # print("=====++++++++++++++=====")

        if max_value == 0:
            best_move = self.select_random_piece(available_pieces)

        #if max_value is 0, have it select a random piece to move instead
        return best_move

    def make_best_move(self):
        piece, move = self.evaluate()
        if piece is not None and move is not None:
            self.move_piece(piece, move)

        print("=========================")
        print(f"Piece: {piece}, Value: {move}")
        print("=========================")

        return piece, move

    def add_to_board(self, piece, pos):
        self.board[pos[0]][pos[1]] = piece

    def make_demo_board(self):

        WHT_POS = {
            "bishop": [[0, 2], [0, 5]],
            "knight": [[0, 1], [0, 6]],
            "rook": [[0, 0], [0, 7]],
            "queen": [0, 3],
            "king": [0, 4]
        }

        BLK_POS = {
            "bishop": [[7, 2], [7, 5]],
            "knight": [[7, 1], [7, 6]],
            "rook": [[7, 0], [7, 7]],
            "queen": [7, 3],
            "king": [7, 4]
        }

        allegiance = 'Black'

        # Bishops in Column 2, 4 Row 0
        bishop_1 = p.Bishop(allegiance, self.board, BLK_POS['bishop'][0])
        self.add_to_board(bishop_1, BLK_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self.board, BLK_POS['bishop'][1])
        self.add_to_board(bishop_2, BLK_POS['bishop'][1])

        # # Queen
        queen = p.Queen(allegiance, self.board, BLK_POS['queen'])
        self.add_to_board(queen, BLK_POS['queen'])

        # # King
        king = p.King(allegiance, self.board, BLK_POS['king'])
        self.add_to_board(king, BLK_POS['king'])

        # # Rooks
        rook1 = p.Rook(allegiance, self.board, BLK_POS['rook'][0])
        self.add_to_board(rook1, BLK_POS['rook'][0])

        rook2 = p.Rook(allegiance, self.board, BLK_POS['rook'][1])
        self.add_to_board(rook2, BLK_POS['rook'][1])

        # # Knight
        knight1 = p.Knight(allegiance, self.board, BLK_POS['knight'][0])
        self.add_to_board(knight1, BLK_POS['knight'][0])

        knight2 = p.Knight(allegiance, self.board, BLK_POS['knight'][1])
        self.add_to_board(knight2, BLK_POS['knight'][1])

        # Pawn
        for col in range(8):
            pawn = p.Pawn(allegiance, self.board, [6, col])
            self.add_to_board(pawn, [6, col])

        # Bishops in Column 2, 4 Row 0
        allegiance = 'White'

        bishop_1 = p.Bishop(allegiance, self.board, WHT_POS['bishop'][0])
        self.add_to_board(bishop_1, WHT_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self.board, WHT_POS['bishop'][1])
        self.add_to_board(bishop_2, WHT_POS['bishop'][1])

        # # Queen
        queen = p.Queen(allegiance, self.board, WHT_POS['queen'])
        self.add_to_board(queen, WHT_POS['queen'])

        # King
        king = p.King(allegiance, self.board, WHT_POS['king'])
        self.add_to_board(king, WHT_POS['king'])

        #Rooks
        rook1 = p.Rook(allegiance, self.board, WHT_POS['rook'][0])
        self.add_to_board(rook1, WHT_POS['rook'][0])

        rook2 = p.Rook(allegiance, self.board, WHT_POS['rook'][1])
        self.add_to_board(rook2, WHT_POS['rook'][1])

        # #Knight
        knight1 = p.Knight(allegiance, self.board, WHT_POS['knight'][0])
        self.add_to_board(knight1, WHT_POS['knight'][0])

        knight2 = p.Knight(allegiance, self.board, WHT_POS['knight'][1])
        self.add_to_board(knight2, WHT_POS['knight'][1])

        # demoPawn = p.Pawn(allegiance, self.board, [0, 0])
        # demoPawn.capture()
        # self.white_capture_board[0][0] = demoPawn

        # Pawn
        for col in range(8):
            pawn = p.Pawn(allegiance, self.board, [1, col])
            self.add_to_board(pawn, [1, col])

    def print_board(self):
        for row in reversed(self.board):
            printable_row = [0 if square is None else square for square in row]
            print(printable_row)



# Example usage:
# Initialize your board and computer player
# board = [[None for _ in range(8)] for _ in range(8)]
# computer_player = Computer('Black', board)

# computer_player.make_best_move()
# computer_player.print_board()