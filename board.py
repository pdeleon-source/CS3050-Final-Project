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
VALID_MOVE_COLOR = arcade.color.GREEN
VALID_CAPTURE_COLOR = arcade.color.RED

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

#p = pieces.Piece


class Board(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Chessboard")

        self.valid_moves = []
        self.capture_moves = []

        arcade.set_background_color(arcade.color.WHITE)
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.selected_piece = None
        self.selected_row = 0
        self.selected_col = 0

        # 2D list to keep track of whether each square is selected
        # I made this separate from the board array, since the board array
        # will have piece classes. We can change this later if needed
        self.selected = [[False for _ in range(COLS)] for _ in range(ROWS)]

        # Create Pieces and add pieces to board
        self.make_black_set()
        self.make_white_set()

        # Give player pieces

    def on_draw(self):
        arcade.start_render()

        # Make even squares
        square_width = SCREEN_WIDTH // COLS
        square_height = SCREEN_HEIGHT // ROWS

        for row in range(ROWS):
            for col in range(COLS):
                x = col * square_width
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

                # Draw the piece if it exists at this position
                piece = self.board[row][col]
                if isinstance(piece, p.Piece):
                    arcade.draw_texture_rectangle(x + square_width // 2, y + square_height // 2, square_width,
                                                  square_height, piece.texture)

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
        square_width = SCREEN_WIDTH // COLS
        square_height = SCREEN_HEIGHT // ROWS

        # Map to corresponding column and row
        col = x // square_width
        row = y // square_height

        # If a piece is selected
        if any(self.selected[row][col] for row in range(ROWS) for col in range(COLS)):

            # If the clicked spot is a valid move
            if (row, col) in self.valid_moves:
                # Move the selected piece to the clicked spot
                self.move_piece(row, col)

            # If the clicked spot is another piece
            elif isinstance(self.board[row][col], p.Piece):
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
                self.valid_moves = []
                self.capture_moves = []
        # If no piece is selected
        else:
            # If the clicked spot contains a piece
            if isinstance(self.board[row][col], p.Piece):
                # Select the piece
                self.deselect_all()
                self.selected[row][col] = True
                self.selected_piece = self.board[row][col]
                self.selected_row = row
                self.selected_col = col
                # Find valid moves for the selected piece
                piece = self.board[row][col]
                self.valid_moves, self.capture_moves = piece.available_moves()

        # Print out Console Board with toggled Squares
        # print("===============================")
        # self.print_board()
        # print("===============================\n\n")


    def print_board(self):
        [print(row) for row in reversed(self.board)]

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
        # rook1 = p.Rook(allegiance, self.board, BLK_POS['rook'][0])
        # self.add_to_board(rook1, BLK_POS['rook'][0])
        #
        # rook2 = p.Rook(allegiance, self.board, BLK_POS['rook'][1])
        # self.add_to_board(rook2, BLK_POS['rook'][1])

        #Pawn
        # for col in range(COLS):
        #     pawn = p.Pawn(allegiance, self.board, [1, col])
        #     self.add_to_board(pawn, [1, col])

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

        # Rooks
        # rook1 = p.Rook(allegiance, self.board, WHT_POS['rook'][0])
        # self.add_to_board(rook1, WHT_POS['rook'][0])

        # rook2 = p.Rook(allegiance, self.board, WHT_POS['rook'][1])
        # self.add_to_board(rook2, WHT_POS['rook'][1])

        # Pawn
        # for col in range(COLS):
        #     pawn = p.Pawn(allegiance, self.board, [6, col])
        #     self.add_to_board(pawn, [6, col])
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


    def move_piece(self, row, col):
        self.valid_moves = []
        self.capture_moves = []
        self.board[self.selected_row][self.selected_col] = None
        self.board[row][col] = self.selected_piece
        self.selected_piece.move([row, col], self.board)
        self.deselect_all()

