# TODO: Prioritize Capture over random position :)
# ^^ Knight becomes kind of a problem...but its fine!!


import random
from pieces import Piece
import pieces as p
import numpy as np
from copy import copy

SQUARE_WIDTH = 400 // 8
SQUARE_HEIGHT = 400 // 8


# this will be a class that can move pieces legally around the chess board
# Note: Doesn't have to be smart, just has to be "correct"
class Computer:
    def __init__(self, allegiance: str, board):
        self.board_array = board

        self.allegiance = allegiance
        self.demo_board = copy(board)
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

    def temp_select_piece(self, allegiance):
        available_pieces = []
        # for each square in the array representing the board
        for row in self.demo_board:
            for square in row:
                # if it has a piece
                if square is not None:
                    # check if the piece is of the correct color
                    if square.allegiance == allegiance:
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

    # def select_random_piece(self, available_pieces):
    #     # Check for capturing moves first
    #     capturing_moves = [piece for piece in available_pieces if piece.available_captures()]
    #     if capturing_moves:
    #         piece_selection = random.choice(capturing_moves)
    #     else:
    #         piece_selection = random.choice(available_pieces)
    #
    #     # Select a random valid move for the selected piece
    #     possible_moves, possible_captures, _ = piece_selection.available_moves()
    #     all_moves = possible_moves + possible_captures
    #     random_move = random.choice(all_moves)
    #     return piece_selection, random_move
    
    # computer player will move a piece
    # use select_piece() and feed it in to the piece param
    def move_piece(self, piece: Piece, move_coords):

        # Store the piece's current position
        current_row = piece.current_row
        current_col = piece.current_col

        # Move piece to square
        valid_move = piece.move(move_coords)

        # Update the piece's position in the board_array
        if valid_move:
            print(f"moved {piece} from [{current_row} {current_col}]")
            self.board_array[current_row][current_col] = None
            self.board_array[move_coords[0]][move_coords[1]] = piece

    def template_move_piece(self, piece: Piece, move_coords):

        # Store the piece's current position
        current_row = piece.temp_current_row
        current_col = piece.temp_current_col

        # Move piece to square
        self.demo_board = piece.template_move(move_coords, self.demo_board)

        # Update the piece's position in the board_array
        self.demo_board[current_row][current_col] = None
        self.demo_board[move_coords[0]][move_coords[1]] = piece

    def evaluate(self, depth):
        best_move = []
        max_score = float('-inf')

        available_pieces = self.select_piece()
        for piece in available_pieces:
            possible_moves, possible_captures, attacks = piece.available_moves()
            old_position = [piece.temp_current_row, piece.temp_current_col]
            print("=========================")
            print(f"Piece: {piece}")
            for new_position in possible_moves + possible_captures:
                old_value = self.demo_board[new_position[0]][new_position[1]]

                # Simulate the move
                self.template_move_piece(piece, new_position)
                score = self.minimax(depth - 1, False, piece, new_position)  # Opponent's turn

                print(f"Value: {score}")
                print("=========================")
                # Undo the move
                self.demo_board[old_position[0]][old_position[1]] = piece
                self.demo_board[new_position[0]][new_position[1]] = old_value

                # TODO: Figure out some logic here
                # Computer should do the move that will get the player the LEAST amount of points
                # Currently it's doing moves that will get player the most points <-- aka bad? i think??
                if score > max_score:
                    max_score = score
                    # New Low Min-Score, so reset the list of best moves
                    best_move = []
                    best_move.append((piece, new_position))
                elif score == max_score:
                    # Add additional best-move to list
                    best_move.append((piece, new_position))

        return best_move

    def get_best(self, moves):
        max_points = float('-inf')
        best_move = None

        for move in moves:
            piece, position = move
            target_piece = self.board_array[position[0], position[1]]
            if target_piece is not None:
                score = target_piece.get_value()
                if score > max_points:
                    max_points = score
                    best_move = (piece, position)
            else:
                if max_points < 0:
                    max_points = 0

        if max_points == 0:
            selection = random.randrange(0, len(moves))
            best_move = moves[selection]

        return best_move


    def make_best_move(self, depth):
        self.demo_board = copy(self.board_array)
        best_moves = self.evaluate(depth)

        piece, move = self.get_best(best_moves)

        if piece is not None and move is not None:
            self.move_piece(piece, move)

        print("=========================")
        print(f"Piece: {piece}, Move: {move}")
        print("=========================")

        return piece, move

    def minimax(self, depth, is_maximizing_player, curr_piece, position):
        if depth == 0:

            # Evaluate the position
            target_piece = self.demo_board[position[0]][position[1]]
            return target_piece.get_value() if target_piece is not None else 0

        if is_maximizing_player:
            # Computer's Turn
            max_eval = float('-inf')
            best_move = None
            available_pieces = self.temp_select_piece("Black")
            for piece in available_pieces:
                possible_moves, possible_captures, attacks = piece.available_moves()
                old_position = [piece.temp_current_row, piece.temp_current_col]
                for new_position in possible_moves + possible_captures:
                    # Simulate the move
                    old_value = self.demo_board[new_position[0]][new_position[1]]

                    # move = new position
                    # self.template_move_piece(piece, new_position)

                    eval = self.minimax(depth - 1, False, piece, new_position)  # Opponent's turn

                    # Undo the move
                    # self.demo_board[old_position[0]][old_position[1]] = piece
                    # self.demo_board[new_position[0]][new_position[1]] = old_value

                    if eval < max_eval:
                        max_eval = eval
                        best_move = (piece, new_position)
                        # print(f"New best move for black: {best_move}, Eval: {min_eval}")

            if best_move:
                print(f"Best move for black: {best_move}, Eval: {max_eval}")
                self.template_move_piece(best_move[0], best_move[1])
                best_move = None
            return max_eval
        else:
            # Human's Turn
            min_eval = float('inf')
            best_move = None
            available_pieces = self.temp_select_piece("White")
            for piece in available_pieces:
                possible_moves, possible_captures, attacks = piece.available_moves()
                old_position = (piece.temp_current_row, piece.temp_current_col)

                for move in possible_moves + possible_captures:
                    # Simulate the move
                    old_value = self.demo_board[move[0]][move[1]]

                    eval = self.minimax(depth - 1, True, piece, move)  # Computer's turn
                    # self.template_move_piece(piece, move)
                    #
                    #
                    # # Undo the move
                    # self.demo_board[old_position[0]][old_position[1]] = piece
                    # self.demo_board[move[0]][move[1]] = old_value

                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)
                        # print(f"New best move for white: {best_move}, Eval: {max_eval}")

            if best_move:
                print(f"Best move for white: {best_move}, Eval: {min_eval}")
                self.template_move_piece(best_move[0], best_move[1])
                best_move = None

            return min_eval

    def evaluate_position(self):
        # Evaluate the position based on piece values, board control, etc.
        return random.randint(0, 100)  # Placeholder evaluation function

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