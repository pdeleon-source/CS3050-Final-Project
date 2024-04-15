"""
Chess AI Logic
"""

import random
from pieces import Piece

from copy import copy
import arcade
from sound_manager import ManageSound

# Get screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

# Set dimensions for the chessboard
BOARD_WIDTH = 800
BOARD_HEIGHT = 600

# Calculate square dimensions based on board size
SQUARE_WIDTH = (BOARD_WIDTH - 200) // 8
SQUARE_HEIGHT = BOARD_HEIGHT // 8

class Computer:
    def __init__(self, allegiance: str, board):
        """
        Initialize the Computer object.

        Parameters:
        - allegiance (str): The allegiance of the computer player ("White" or "Black").
        - board: The game board representing the current game state.
        """
        self.board_array = board

        self.allegiance = allegiance
        self.demo_board = copy(board)
        self.sound_manager = ManageSound(1)
        # self.make_demo_board()

    # computer player will select a piece; returns a piece object
    def select_piece(self):
        """
        Select a piece to move.

        Returns:
        - available_pieces (list): List of available pieces for the computer player to move.
        """
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
        """
        Temporary selection of pieces for simulation.

        Parameters:
        - allegiance (str): The allegiance of the pieces to select ("White" or "Black").

        Returns:
        - available_pieces (list): List of available pieces for simulation.
        """
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

    def template_move_piece(self, piece: Piece, move_coords):
        """
        Simulate moving a piece for evaluation.

        Parameters:
        - piece (Piece): The piece object to simulate moving.
        - move_coords (list): Coordinates of the simulated move.

        Returns:
        - None
        """

        # Store the piece's current position
        current_row = piece.temp_current_row
        current_col = piece.temp_current_col

        # Move piece to square
        self.demo_board = piece.template_move(move_coords, self.demo_board)

        # Update the piece's position in the board_array
        self.demo_board[current_row][current_col] = None
        self.demo_board[move_coords[0]][move_coords[1]] = piece

    def evaluate(self, depth):
        """
        Evaluate possible moves based on a given depth.

        Parameters:
        - depth (int): The depth of evaluation for the minimax algorithm.

        Returns:
        - best_move (list): List of the best moves determined by evaluation.
        """
        best_move = []
        max_score = float('-inf')

        available_pieces = self.select_piece()
        for piece in available_pieces:
            possible_moves, possible_captures, attacks = piece.available_moves(False)
            for new_position in possible_moves + possible_captures:

                # Simulate the move
                score = self.minimax(depth - 1, False, piece, new_position)  # Opponent's turn

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
        """
        Get the best move from a list of moves.

        Parameters:
        - moves (list): List of moves to evaluate.

        Returns:
        - best_move (tuple): Tuple containing the best move and its piece.
        """
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
        """
        Make the best move based on evaluation depth.

        Parameters:
        - depth (int): Depth of evaluation for the best move.

        Returns:
        - piece (Piece): The piece selected for the best move.
        - move (list): Coordinates of the best move.
        - is_cap (bool): Whether the move results in a capture.
        - capped_piece (Piece): The piece captured (if any).
        """
        is_cap = False
        capped_piece = None
        self.demo_board = copy(self.board_array)
        best_moves = self.evaluate(depth)

        piece, move = self.get_best(best_moves)

        if self.board_array[move[0]][move[1]] != self.allegiance and self.board_array[move[0]][move[1]] is not None:
            is_cap = True
            capped_piece = self.board_array[move[0]][move[1]]

        return piece, move, is_cap, capped_piece

    def minimax(self, depth, is_maximizing_player, curr_piece, position):
        """
        Minimax algorithm for evaluating moves.

        Parameters:
        - depth (int): Depth of evaluation for the minimax algorithm.
        - is_maximizing_player (bool): Flag indicating if the player is maximizing the score.
        - curr_piece (Piece): Current piece being evaluated.
        - position (list): Coordinates of the move.

        Returns:
        - eval (int): Evaluation score for the move.
        """
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
                for new_position in possible_moves + possible_captures:

                    eval = self.minimax(depth - 1, False, piece, new_position)  # Opponent's turn

                    if eval < max_eval:
                        max_eval = eval
                        best_move = (piece, new_position)

            if best_move:
                self.template_move_piece(best_move[0], best_move[1])
            return max_eval
        else:
            # Human's Turn
            min_eval = float('inf')
            best_move = None
            available_pieces = self.temp_select_piece("White")
            for piece in available_pieces:
                possible_moves, possible_captures, attacks = piece.available_moves(False)

                for move in possible_moves + possible_captures:

                    eval = self.minimax(depth - 1, True, piece, move)  # Computer's turn

                    if eval < min_eval:
                        min_eval = eval
                        best_move = (piece, move)

            if best_move:
                self.template_move_piece(best_move[0], best_move[1])

            return min_eval