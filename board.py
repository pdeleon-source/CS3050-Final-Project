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

from datetime import datetime, timedelta


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

CAPTURE_BOX = 100 // 4

# Set the colors for the chessboard squares
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN
SELECTED_SQUARE_COLOR = arcade.color.CYAN
VALID_MOVE_COLOR = arcade.color.GREEN
VALID_CAPTURE_COLOR = arcade.color.RED

GAME_DURATION = timedelta(minutes=10)  # Total game duration

BLACK_TIMER_POSITION = (50, SCREEN_HEIGHT - 50)
WHITE_TIMER_POSITION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - (SCREEN_HEIGHT - 50))
TIMER_FONT_SIZE = 9

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

# Sound effects
MOVE_SOUND = "sounds/checkmate.wav"
# p = pieces.Piece
white_allegiance = "White"
black_allegiance = "Black"

class Board(arcade.View):
    # TODO: Pass in list of theme colors or string representing theme?
    # TODO: Pass in sound on or off?
    def __init__(self, versus, theme):
        super().__init__()
        self.versus = versus
        # Add a variable to track whose turn it is
        self.current_turn = white_allegiance  # Start with white's turn

        self.valid_moves = []
        self.capture_moves = []
        self.captures = []
        self.white_capture_board = np.array([[None for _ in range(4)] for _ in range(4)])
        self.black_capture_board = np.array([[None for _ in range(4)] for _ in range(4)])

        arcade.set_background_color(arcade.color.WHITE)
        self.board = np.array([[None for _ in range(COLS)] for _ in range(ROWS)])
        self.prev_board = copy.copy(self.board)
        self.selected_piece = None
        self.computer_piece = None
        self.captured_piece = None
        self.selected_row = None
        self.selected_col = None

        self.WHITE_TIME = timedelta(minutes=5)
        self.BLACK_TIME = timedelta(minutes=5)
        self.current_turn_start = None

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

        # TODO: Pass in theme manager object instead?
        """Set colors based on theme"""
        if theme == "midnight":
            self.light_square_color = arcade.color.QUEEN_BLUE
            self.dark_square_color = arcade.color.DARK_MIDNIGHT_BLUE
            self.bg_color = arcade.color.MIDNIGHT_BLUE
        elif theme == "pink":
            self.light_square_color = arcade.color.CAMEO_PINK
            self.dark_square_color = arcade.color.CHINA_PINK
            self.bg_color = arcade.color.DUST_STORM
        elif theme == "ocean":
            self.light_square_color = arcade.color.PALE_ROBIN_EGG_BLUE
            self.dark_square_color = arcade.color.DARK_CYAN
            self.bg_color = arcade.color.MEDIUM_AQUAMARINE
        else: # Default colors
            self.light_square_color = arcade.color.ALMOND
            self.dark_square_color = arcade.color.SADDLE_BROWN
            self.bg_color = arcade.color.BRUNSWICK_GREEN
        self.theme = theme
    def on_show(self):
        arcade.set_background_color(self.bg_color)

        # self.chess_piece.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def update(self, delta_time):
        if self.current_turn_start is not None:
            elapsed_time = datetime.now() - self.current_turn_start
            if self.current_turn == white_allegiance:
                self.WHITE_TIME -= elapsed_time
            else:
                self.BLACK_TIME -= elapsed_time

            # Check if time has run out for either player
            if self.WHITE_TIME <= timedelta(seconds=0):
                print("White time ran out. Black wins!")
                # Handle end of game
            elif self.BLACK_TIME <= timedelta(seconds=0):
                print("Black time ran out. White wins!")
                # Handle end of game

            self.current_turn_start = datetime.now()

        if self.selected_piece is not None:
            self.selected_piece.update()
            if self.selected_piece.x == self.selected_piece.target_x and self.selected_piece.y == self.selected_piece.target_y:
                if self.computer_piece is not None:
                    self.computer_piece.update()
                    if self.captured_piece is not None:
                        self.captured_piece.update()

    def on_draw(self):
        arcade.start_render()



        # Make even squares
        square_width = (SCREEN_WIDTH - 200) // COLS
        square_height = SCREEN_HEIGHT // ROWS

        if self.theme == "midnight":
            background = arcade.load_texture("pieces_png/midnight.jpg")
            background.draw_sized(center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT/2,
                                  width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

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
                    color = self.light_square_color
                else:
                    color = self.dark_square_color

                arcade.draw_rectangle_filled(x + square_width // 2, y + square_height // 2, square_width, square_height,
                                             color)
        for row in range(ROWS):
            for col in range(COLS):
                # Draw the piece if it exists at this position
                piece = self.board[row][col]

                if isinstance(piece, p.Piece):
                    piece.draw()

        for row in range(4):
            for col in range(4):
                # Draw the piece if it exists at this position
                white_piece = self.white_capture_board[row][col]
                black_piece = self.black_capture_board[row][col]

                if isinstance(white_piece, p.Piece):
                    white_piece.draw()
                if isinstance(black_piece, p.Piece):
                    black_piece.draw()

        # for col in range(COLS):
        #     label = chr(ord('a') + col)  # Convert column index to corresponding letter
        #     x = col * square_width + square_width // 2
        #     y = SCREEN_HEIGHT - 20
        #     arcade.draw_text(label, x, y, arcade.color.BLACK, 12, anchor_x="center")

        # # Draw labels for rows (1-8)
        # for row in range(ROWS):
        #     label = str(row + 1)  # Convert row index to corresponding number
        #     x = SCREEN_WIDTH - 20
        #     y = row * square_height + square_height // 2
        #     arcade.draw_text(label, x, y, arcade.color.BLACK, 12, anchor_x="center", anchor_y="center")

        # Draw the timers for white and black players
        self.draw_timer(WHITE_TIMER_POSITION, self.WHITE_TIME, "White's")
        self.draw_timer(BLACK_TIMER_POSITION, self.BLACK_TIME, "Black's")

    def draw_timer(self, position, remaining_time, player):
        title_text = f"{player} Timer:"
        timer_text = f"{remaining_time.seconds // 60:02d}:{remaining_time.seconds % 60:02d}"
        arcade.draw_text(title_text, position[0], position[1], arcade.color.BLACK, TIMER_FONT_SIZE, anchor_x="center")
        arcade.draw_text(timer_text, position[0], position[1] - TIMER_FONT_SIZE * 2, arcade.color.BLACK, TIMER_FONT_SIZE, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        global current_turn_start

        # Start the timer when a player makes a move
        self.current_turn_start = datetime.now()

        # Square boundaries
        square_width = (SCREEN_WIDTH - 200) // COLS
        square_height = SCREEN_HEIGHT // ROWS

        # Map to corresponding column and row
        col = (x - 100) // square_width
        row = y // square_height

        # Init sound
        audio = arcade.load_sound(MOVE_SOUND, False)

        # If a piece is selected
        # if self.current_turn == white_allegiance:
        if any(self.selected[r][c] for r in range(ROWS) for c in range(COLS)):
            # If the clicked spot is a valid move
            if (row, col) in self.valid_moves:
                # Move the selected piece to the clicked spot
                self.move_piece(row, col)
                arcade.play_sound(audio, 1.0, -1, False)
            # If the clicked spot is a capture move
            elif (row, col) in self.capture_moves:
                # Record capture in list
                #self.imprison_piece(self.board[row][col])
                self.make_capture(self.board[row][col])
                #self.captures.append(self.board[row][col])
                self.captured_piece = self.board[row][col]
                # Move the selected piece to the clicked spot
                self.move_piece(row, col)
                #arcade.play_sound(audio, 1.0, -1, False)

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
                    self.valid_moves, self.capture_moves, self.attack_moves = piece.available_moves()

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
                    self.valid_moves, self.capture_moves, self.attack_moves = piece.available_moves()
                    # print(self.valid_moves, self.capture_moves)

        # Print out Console Board with toggled Squares
        # print("===============================")
        # self.print_board()
        # print("===============================\n\n")

    def print_board(self):
        for row in reversed(self.board):
            printable_row = [0 if square is None else square for square in row]
            print(printable_row)

    def print_capture(self):
        for row in reversed(self.white_capture_board):
            printable_row = [0 if square is None else square for square in row]
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
        for col in range(COLS):
            pawn = p.Pawn(allegiance, self.board, [6, col])
            self.add_to_board(pawn, [6, col])

    def make_white_set(self):
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
        self.selected_piece.move([row, col])

        """ Check if move is en passant """
        cap = self.selected_piece.en_passant([row, col])
        if cap is not None:
            # self.captures.append(self.board[cap[0]][cap[1]])
            # self.imprison_piece(self.board[cap[0]][cap[1]])
            self.make_capture(self.board[cap[0]][cap[1]])
            self.captured_piece = self.board[row][col]
            self.board[cap[0]][cap[1]] = None

        """ Change to queen if pawn promotable
        if self.selected_piece.promotable():
            queen = p.Queen(self.selected_piece.allegiance, self.board, self.board[row][col])
            self.board[row][col] = queen
        else:
            self.board[row][col] = piece
        """

        self.board[self.selected_row][self.selected_col] = None
        self.board[row][col] = piece


        # Wait for the animation to finish
        # time.sleep(1)  # Adjust the delay as needed

        self.deselect_all()

        print("============= Whites Turn ===========")
        self.print_board()
        if piece.allegiance == 'White':
            self.check_game_over('Black')
        else:
            self.check_game_over('White')
        self.print_capture()
        self.switch_turn()

    def switch_turn(self):
        # Switch the turn between white and black
        if self.current_turn == white_allegiance:
            self.current_turn = black_allegiance
        else:
            self.current_turn = white_allegiance

        self.current_turn_start = datetime.now()  # Start the timer for the new turn

        # Handle computer's turn if necessary
        if self.current_turn == black_allegiance and self.versus == "computer":
            self.handle_computer_turn()

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
            print("CAPTURES")
            self.print_capture()
            if computer_piece.allegiance == 'White':
                self.check_game_over('Black')
            else:
                self.check_game_over('White')
            self.switch_turn()
    def make_capture(self, piece):
        allegiance = piece.allegiance
        offset = CAPTURE_BOX // 2

        for row in range(4):
            for col in range(4):
                if piece.allegiance == "White":
                    if self.white_capture_board[row][col] is None:
                        x = col * CAPTURE_BOX + (SCREEN_WIDTH - 100)
                        y = row * CAPTURE_BOX + (SCREEN_HEIGHT - 100)
                        self.white_capture_board[row][col] = piece
                        piece.update_target(x, y)
                        self.captured_piece = piece
                        return
                elif piece.allegiance == "Black":
                    if self.black_capture_board[row][col] is None:
                        x = col * CAPTURE_BOX # + (SCREEN_WIDTH - 100)
                        y = row * CAPTURE_BOX # + (SCREEN_HEIGHT - 100)
                        self.black_capture_board[row][col] = piece
                        piece.update_target(x, y)
                        self.captured_piece = piece
                        return





    # This function will check if a side is in checkmate
    # This will end the game and declare a winner
    def check_game_over(self, allegiance):
        # get all the pieces of a specific allegiance
        pieces = []
        # for each square
        for row in range(ROWS):
            for col in range(COLS):
                # if the square has a piece
                if isinstance(self.board[row][col], p.Piece):
                    # if that piece is of the correct allegiance, save it
                    if self.board[row][col].allegiance == allegiance:
                        pieces.append(self.board[row][col])


        king_in_check = False
        for i in pieces:
            # if that piece is the king, check if it is in check
            if isinstance(i, p.King):
                king_in_check = i.under_attack(i.current_row, i.current_col)

        all_moves = []
        for i in pieces:
            moves, caps, attacks = i.available_moves()
            # record if each piece has any moves available
            for j in moves:
                all_moves.append(j)

            for k in caps:
                all_moves.append(k)

        # print('MOVES: ', all_moves)
        print('CHECK: ', king_in_check)

        # if there are no possible moves and the king is in check
        if all_moves == [] and king_in_check:
            # end the game, other side wins
            if pieces[0].allegiance == 'White':
                print('Black wins!')
            else:
                print('White wins!')
            # TODO: End the game
            # I'm thinking this gives an end game screen that says who won (if anyone did)
            # and a button to view the board or quit back to menu
            # If the user views the board, they should still have a button to return to menu
            exit()

        # if there are no possible moves and the king is NOT in check
        elif all_moves == [] and not king_in_check:
            # end the game, draw
            print("It's a draw!")
            # TODO: End the game
            # I'm thinking this gives an end game screen that says who won (if anyone did)
            # and a button to view the board or quit back to menu
            # If the user views the board, they should still have a button to return to menu
            exit()



        # print("PIECES")
        # print(pieces)