# Board Class

import arcade
import pieces as p

# Set the dimensions of the chessboard
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
ROWS = 8
COLS = 8

# Set the colors for the chessboard squares
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN
SELECTED_SQUARE_COLOR = arcade.color.CYAN

# Set containing all black piece default positions
BLK_POS = {
    "bishop": [[0, 2], [0, 5]],
    "knight": [[0, 1], [0, 6]],
    "rook": [[0, 0], [0, 7]],
    "queen": [0, 3],
    "king": [0, 4]
}

WHT_POS = {
    "bishop": [[7, 2], [7, 5]],
    "knight": [[7, 1], [7, 6]],
    "rook": [[7, 0], [7, 7]],
    "queen": [7, 3],
    "king": [7, 4]
}


class Board(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Chessboard")

        arcade.set_background_color(arcade.color.WHITE)
        self.board = [['_' for _ in range(COLS)] for _ in range(ROWS)]

        # 2D list to keep track of whether each square is selected
        # I made this separate from the board array, since the board array
        # will have piece classes. We can change this later if needed
        self.selected = [[False for _ in range(COLS)] for _ in range(ROWS)]

        # Create Pieces
        self.make_black_set()
        self.make_white_set()

        # Add Pieces To board

    def on_draw(self):
        arcade.start_render()

        # Make even squares
        square_width = SCREEN_WIDTH // COLS
        square_height = SCREEN_HEIGHT // ROWS



        for row in range(ROWS):
            for col in range(COLS):
                x = col * square_width
                y = row * square_height
                if self.selected[row][col]:
                    color = SELECTED_SQUARE_COLOR
                    print(self.board[row][col].get_movement_pattern())
                elif (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR
                arcade.draw_rectangle_filled(x + square_width // 2, y + square_height // 2, square_width, square_height,
                                             color)

                # Draw the piece if it exists at this position
                piece = self.board[row][col]
                if not isinstance(piece, str):
                    arcade.draw_texture_rectangle(x + square_width // 2, y + square_height // 2, square_width,
                                                  square_height, piece.texture)

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
        square_width = SCREEN_WIDTH // COLS
        square_height = SCREEN_HEIGHT // ROWS

        # Map to corresponding column and row
        col = x // square_width
        row = y // square_height

        # Toggle the selected state of the clicked square
        self.selected[row][col] = not self.selected[row][col]

        # Print out Console Board with toggled Squares
        print("===============================")
        self.print_board()
        print("===============================\n\n")

    def print_board(self):
        [print(row) for row in reversed(self.board)]

    def add_to_board(self, piece, pos):
        self.board[pos[0]][pos[1]] = piece

    def make_black_set(self):
        allegiance = 'Black'

        # Bishops in Column 2, 4 Row 0
        bishop_1 = p.Bishop(allegiance, self, BLK_POS['bishop'][0])
        self.add_to_board(bishop_1, BLK_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self, BLK_POS['bishop'][1])
        self.add_to_board(bishop_2, BLK_POS['bishop'][1])

        # Queen
        queen = p.Queen(allegiance, self, BLK_POS['queen'])
        self.add_to_board(queen, BLK_POS['queen'])

        # King
        king = p.King(allegiance, self, BLK_POS['king'])
        self.add_to_board(king, BLK_POS['king'])

        return bishop_1, bishop_2

    def make_white_set(self):
        # Bishops in Column 2, 4 Row 0
        allegiance = 'White'

        bishop_1 = p.Bishop(allegiance, self, WHT_POS['bishop'][0])
        self.add_to_board(bishop_1, WHT_POS['bishop'][0])

        bishop_2 = p.Bishop(allegiance, self, WHT_POS['bishop'][1])
        self.add_to_board(bishop_2, WHT_POS['bishop'][1])

        # Queen
        queen = p.Queen(allegiance, self, WHT_POS['queen'])
        self.add_to_board(queen, WHT_POS['queen'])

        # King
        king = p.King(allegiance, self, WHT_POS['king'])
        self.add_to_board(king, WHT_POS['king'])

        return bishop_1, bishop_2


