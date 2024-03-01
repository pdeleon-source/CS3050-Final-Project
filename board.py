# Board Class

import arcade

# Set the dimensions of the chessboard
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
ROWS = 8
COLS = 8

# Set the colors for the chessboard squares
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN
SELECTED_SQUARE_COLOR = arcade.color.CYAN

class Board(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Chessboard")

        arcade.set_background_color(arcade.color.WHITE)
        self.board = [['0' for _ in range(COLS)] for _ in range(ROWS)]

        # 2D list to keep track of whether each square is selected
        # I made this separate from the board array, since the board array
        # will have piece classes. We can change this later if needed
        self.selected = [[False for _ in range(COLS)] for _ in range(ROWS)]

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
                elif (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR
                arcade.draw_rectangle_filled(x + square_width // 2, y + square_height // 2, square_width, square_height, color)

    def on_mouse_press(self, x, y, button, modifiers):

        # Square boundaries
        square_width = SCREEN_WIDTH // COLS
        square_height = SCREEN_HEIGHT // ROWS

        # Map to corresponding column and row
        col = x // square_width
        row = y // square_height

        # Toggle the selected state of the clicked square
        self.selected[row][col] = not self.selected[row][col]

        # Toggle 'X' and '0' in the corresponding row and column of the board
        if self.board[row][col] == 'X':
            self.board[row][col] = '0'

        else:
            self.board[row][col] = 'X'

        # Print out Console Board with toggled Squares
        print("===============================")
        self.print_board()
        print("===============================\n\n")

    def print_board(self):
        [print(row) for row in reversed(self.board)]

