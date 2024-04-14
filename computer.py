# TODO: Prioritize Capture over random position :)
# ^^ Knight becomes kind of a problem...but its fine!!


import random
from pieces import Piece

from copy import copy
import arcade
from sound_manager import ManageSound

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

BOARD_WIDTH = 800
BOARD_HEIGHT = 600

SQUARE_WIDTH = (BOARD_WIDTH - 200) // 8
SQUARE_HEIGHT = BOARD_HEIGHT // 8

# SQUARE_WIDTH = 400 // 8
# SQUARE_HEIGHT = 400 // 8


# this will be a class that can move pieces legally around the chess board
# Note: Doesn't have to be smart, just has to be "correct"
class Computer:
    def __init__(self, allegiance: str, board):
        self.board_array = board

        self.allegiance = allegiance
        self.demo_board = copy(board)
        self.sound_manager = ManageSound(1)
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
            possible_moves, possible_captures, attacks = piece_selection.available_moves(False)
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
        # self.sound_manager.play_move_sound()

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
            possible_moves, possible_captures, attacks = piece.available_moves(False)
            old_position = [piece.temp_current_row, piece.temp_current_col]
            print("=========================")
            print(f"Piece: {piece}")
            for new_position in possible_moves + possible_captures:
                old_value = self.demo_board[new_position[0]][new_position[1]]

                # Simulate the move
                # self.template_move_piece(piece, new_position)
                score = self.minimax(depth - 1, False, piece, new_position)  # Opponent's turn

                # TODO: Figure out what to do with this
                # Add computer position evaluation !!!
                target_piece = self.demo_board[new_position[0]][new_position[1]]
                position_value = target_piece.get_value() if target_piece is not None else 0
                evaluation_board = 0
                if target_piece is not None:
                    if target_piece.allegiance == "White":
                        evaluation_board = target_piece.eval[new_position[0]][new_position[1]]
                    else:
                        evaluation_board = reversed(target_piece.eval)[new_position[0]][new_position[1]]

                score += position_value + evaluation_board
                print(f"Value: {score}")
                print("=========================")
                # Undo the move
                # self.demo_board[old_position[0]][old_position[1]] = piece
                # self.demo_board[new_position[0]][new_position[1]] = old_value

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
        is_cap = False
        capped_piece = None
        self.demo_board = copy(self.board_array)
        best_moves = self.evaluate(depth)

        piece, move = self.get_best(best_moves)

        if self.board_array[move[0]][move[1]] != self.allegiance and self.board_array[move[0]][move[1]] is not None:
            # print("***CAPTURE***")
            is_cap = True
            capped_piece = self.board_array[move[0]][move[1]]


        if piece is not None and move is not None:
            self.move_piece(piece, move)

        print("=========================")
        print(f"Piece: {piece}, Move: {move}")
        print("=========================")

        return piece, move, is_cap, capped_piece

    # Fix alpha beta pruning, need to pass in min and max as parameters, so they can be checked :D
    # Also have the computer assess picking the best move for itself, right now it picks a move
    # that gives the player the least amount of points, i think

    # also alpha-beta/max-min pruning means we can disregard certain brances in the search tree, meaning we can go
    # deeper while not making our poor program explode :D <--- hopefully!!!
    def minimax(self, depth, is_maximizing_player, curr_piece, position):
        if depth == 0:

            # Evaluate the position
            target_piece = self.demo_board[position[0]][position[1]]
            position_value = target_piece.get_value() if target_piece is not None else 0
            if curr_piece.allegiance == "White":
                evaluation_board = curr_piece.eval[position[0]][position[1]]
            else:
                evaluation_board = reversed(curr_piece.eval)[position[0]][position[1]]
            return position_value + evaluation_board

        if is_maximizing_player:
            # Computer's Turn
            max_eval = float('-inf')
            best_move = None
            available_pieces = self.temp_select_piece("Black")
            for piece in available_pieces:
                possible_moves, possible_captures, attacks = piece.available_moves(False)
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
                possible_moves, possible_captures, attacks = piece.available_moves(False)
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

# Example usage:
# Initialize your board and computer player
# board = [[None for _ in range(8)] for _ in range(8)]
# computer_player = Computer('Black', board)


# computer_player.make_best_move()
# computer_player.print_board()
