# Board Class
"""
TODO: Main menu
1) 2 Players
- player name
- player score
2) Play Computer
3) Game
4) Settings
- theme
- sound on or off
- timer on or off
Show who's turn

"""

import arcade

import pieces as p

import computer

import numpy as np

import copy

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Set the dimensions of the chessboard
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROWS = 8
COLS = 8
SQUARE_WIDTH = (SCREEN_WIDTH - 200) // 8
SQUARE_HEIGHT = SCREEN_HEIGHT // 8

# Set the colors for the chessboard squares
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN
SELECTED_SQUARE_COLOR = arcade.color.CYAN
VALID_MOVE_COLOR = arcade.color.GREEN
VALID_CAPTURE_COLOR = arcade.color.RED

# Set containing all black piece default positions
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


# p = pieces.Piece
white_allegiance = "White"
black_allegiance = "Black"

class Board(arcade.View):
    def __init__(self):
        super().__init__()

        # Add a variable to track whose turn it is
        self.current_turn = white_allegiance  # Start with white's turn

        self.valid_moves = []
        self.capture_moves = []

        arcade.set_background_color(arcade.color.WHITE)
        self.board = np.array([[None for _ in range(COLS)] for _ in range(ROWS)])
        self.prev_board = copy.copy(self.board)
        self.selected_piece = None
        self.computer_piece = None
        self.selected_row = None
        self.selected_col = None

        # testing Computer
        # this takes in an allegiance and the board array containing pieces
        self.computer = computer.Computer('Black', self.board)

        # 2D list to keep track of whether each square is selected
        # I made this separate from the board array, since the board array
        # will have piece classes. We can change this later if needed
        self.selected = [[False for _ in range(COLS)] for _ in range(ROWS)]

        # Create Pieces and add pieces to board
        self.make_black_set()
        self.make_white_set()

        # Give player pieces

    def on_show(self):
        arcade.set_background_color(arcade.color.BRUNSWICK_GREEN)
        # self.chess_piece.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def update(self, delta_time):
        if self.selected_piece is not None:
            self.selected_piece.update()
            if self.selected_piece.x == self.selected_piece.target_x and self.selected_piece.y == self.selected_piece.target_y:
                if self.computer_piece is not None:
                    self.computer_piece.update()

    def on_draw(self):
        arcade.start_render()

        # Make even squares
        square_width = (SCREEN_WIDTH - 200) // COLS
        square_height = SCREEN_HEIGHT // ROWS

        for row in range(ROWS):
            for col in range(COLS):
                x = (col * square_width) + 100
                y = row * square_height

                if (row, col) in self.capture_moves:
                    color = VALID_CAPTURE_COLOR
                elif (row, col) in self.valid_moves:
                    color = VALID_MOVE_COLOR
                elif self.selected[row][col]:
                    color = SELECTED_SQUARE_COLOR
                elif (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR

                arcade.draw_rectangle_filled(x + square_width // 2, y + square_height // 2, square_width, square_height,
                                             color)
        for row in range(ROWS):
            for col in range(COLS):
                # Draw the piece if it exists at this position
                piece = self.board[row][col]

                if isinstance(piece, p.Piece):
                    piece.draw()

        # # Draw green squares for valid moves
        # for move in self.valid_moves:
        #     row, col = move
        #     x = col * square_width
        #     y = row * square_height
        #     arcade.draw_rectangle_filled(x + square_width // 2, y + square_height // 2, square_width, square_height,
        #                                  VALID_MOVE_COLOR)


        # Draw labels for columns (a-h)
        for col in range(COLS):
            label = chr(ord('a') + col)  # Convert column index to corresponding letter
            x = col * square_width + square_width // 2
            y = SCREEN_HEIGHT - 20
            arcade.draw_text(label, x, y, arcade.color.BLACK, 12, anchor_x="center")

        # Draw labels for rows (1-8)
        for row in range(ROWS):
            label = str(row + 1)  # Convert row index to corresponding number
            x = SCREEN_WIDTH - 20
            y = row * square_height + square_height // 2
            arcade.draw_text(label, x, y, arcade.color.BLACK, 12, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):

        # Square boundaries
        square_width = (SCREEN_WIDTH - 200) // COLS
        square_height = SCREEN_HEIGHT // ROWS

        # Map to corresponding column and row
        col = (x - 100) // square_width
        row = y // square_height

        # If a piece is selected
        if self.current_turn == white_allegiance:
            if any(self.selected[row][col] for row in range(ROWS) for col in range(COLS)):

                # If the clicked spot is a valid move
                if (row, col) in self.valid_moves:
                    # Move the selected piece to the clicked spot
                    self.move_piece(row, col)
                # If the clicked spot is a capture move
                elif (row, col) in self.capture_moves:
                    # Move the selected piece to the clicked spot
                    self.move_piece(row, col)

                # If the clicked spot is another piece
                elif isinstance(self.board[row][col], p.Piece):
                    if self.board[row][col].allegiance == self.current_turn:
                        # Deselect the previously selected piece
                        self.deselect_all()
                        # Select the new piece
                        self.selected[row][col] = True
                        self.selected_row = row
                        self.selected_col = col
                        self.selected_piece = self.board[row][col]
                        # Find valid moves for the new piece
                        piece = self.board[row][col]
                        self.valid_moves, self.capture_moves = piece.available_moves()

                # If the clicked spot is neither a valid move nor another piece, deselect all squares
                else:
                    self.deselect_all()

            # If no piece is selected
            else:
                # If the clicked spot contains a piece
                if isinstance(self.board[row][col], p.Piece):
                    if self.board[row][col].allegiance == self.current_turn:
                        # Select the piece
                        self.deselect_all()
                        self.selected[row][col] = True
                        self.selected_piece = self.board[row][col]
                        self.selected_row = row
                        self.selected_col = col
                        # Find valid moves for the selected piece
                        piece = self.board[row][col]
                        self.valid_moves, self.capture_moves = piece.available_moves()
                        print(self.valid_moves, self.capture_moves)

        # Print out Console Board with toggled Squares
        # print("===============================")
        # self.print_board()
        # print("===============================\n\n")

    def print_board(self):
        for row in reversed(self.board):
            printable_row = ['_' if square is None else square for square in row]
            print(printable_row)

    def add_to_board(self, piece, pos):
        self.board[pos[0]][pos[1]] = piece

    def make_black_set(self):
        allegiance = 'Black'

        # Bishops in Column 2, 4 Row 0
        bishop_1 = p.Bishop(allegiance, self.board, BLK_POS['bishop'][0])
        self.add_to_board(bishop_1, BLK_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self.board, BLK_POS['bishop'][1])
        self.add_to_board(bishop_2, BLK_POS['bishop'][1])

        # Queen
        queen = p.Queen(allegiance, self.board, BLK_POS['queen'])
        self.add_to_board(queen, BLK_POS['queen'])

        # King
        king = p.King(allegiance, self.board, BLK_POS['king'])
        self.add_to_board(king, BLK_POS['king'])

        # Rooks
        rook1 = p.Rook(allegiance, self.board, BLK_POS['rook'][0])
        self.add_to_board(rook1, BLK_POS['rook'][0])

        rook2 = p.Rook(allegiance, self.board, BLK_POS['rook'][1])
        self.add_to_board(rook2, BLK_POS['rook'][1])

        # Knight
        knight1 = p.Knight(allegiance, self.board, BLK_POS['knight'][0])
        self.add_to_board(knight1, BLK_POS['knight'][0])

        knight2 = p.Knight(allegiance, self.board, BLK_POS['knight'][1])
        self.add_to_board(knight2, BLK_POS['knight'][1])

        # Pawn
        for col in range(COLS):
            pawn = p.Pawn(allegiance, self.board, [6, col])
            self.add_to_board(pawn, [1, col])

    def make_white_set(self):
        # Bishops in Column 2, 4 Row 0
        allegiance = 'White'

        bishop_1 = p.Bishop(allegiance, self.board, WHT_POS['bishop'][0])
        self.add_to_board(bishop_1, WHT_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self.board, WHT_POS['bishop'][1])
        self.add_to_board(bishop_2, WHT_POS['bishop'][1])

        # Queen
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

        #Knight
        knight1 = p.Knight(allegiance, self.board, WHT_POS['knight'][0])
        self.add_to_board(knight1, WHT_POS['knight'][0])

        knight2 = p.Knight(allegiance, self.board, WHT_POS['knight'][1])
        self.add_to_board(knight2, WHT_POS['knight'][1])

        # Pawn
        for col in range(COLS):
            pawn = p.Pawn(allegiance, self.board, [1, col])
            self.add_to_board(pawn, [1, col])
        # self.add_to_board(pawn, [4, 5])

    # def check_valid_moves(self, movement):
    #     valid_moves = []
    #     for move in movement:
    #         if not isinstance(self.board[move[0]][move[1]], p.Piece):
    #             valid_moves.append(move)
    #         elif self.board[move[0]][move[1]].allegiance != self.selected_piece.allegiance:
    #             valid_moves.append(move)
    #     return valid_moves

    def deselect_all(self):
        # Deselect all squares
        for row in range(ROWS):
            for col in range(COLS):
                self.selected[row][col] = False

        self.selected_col = None
        self.selected_row = None
        # self.selected_piece = None
        self.valid_moves = []
        self.capture_moves = []

    def move_piece(self, row, col):
        # Get the piece object
        piece = self.board[self.selected_row][self.selected_col]

        self.selected_piece.on_click(col * SQUARE_WIDTH - 37, row * SQUARE_HEIGHT - 35)

        # Deselect the piece and switch turn after animation is complete
        self.selected_piece.move(row, col)

        self.board[self.selected_row][self.selected_col] = None
        self.board[row][col] = piece

        # Wait for the animation to finish
        # time.sleep(1)  # Adjust the delay as needed

        self.deselect_all()

        print("============= Whites Turn ===========")
        self.print_board()
        self.switch_turn()

    def switch_turn(self):
        # Switch the turn between white and black
        if self.current_turn == white_allegiance:
            self.current_turn = black_allegiance
            self.handle_computer_turn()
        else:
            self.current_turn = white_allegiance

    def handle_computer_turn(self):
        # Handle computer input for black's turn
        if self.current_turn == black_allegiance:
            computer_moved = False
            computer_piece = None
            coords = []
            while not computer_moved:
                computer_piece = self.computer.select_piece()
                row = computer_piece.current_row
                col = computer_piece.current_col
                coords = self.computer.move_piece(computer_piece)
                if coords != 4:
                    computer_moved = True

                    self.computer_piece = computer_piece
                    self.computer_piece.on_click(coords[1] * SQUARE_WIDTH - 37, coords[0] * SQUARE_HEIGHT - 35)

            print("============= Blacks Turn ============")
            self.print_board()

            self.switch_turn()

