# Board Class

import arcade

import arcade.gui

import pieces as p

import computer

import numpy as np

import copy

from datetime import datetime, timedelta

import menu as menu

import tutorial as t
import setting as s

from theme_manager import ManageTheme
from game_manager import ManageGame
from sound_manager import ManageSound

import win_lose_menu as w

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 5

# Set the dimensions of the chessboard
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

BOARD_WIDTH = 800
BOARD_HEIGHT = 600
ROWS = 8
COLS = 8
SQUARE_WIDTH = (BOARD_WIDTH - 200) // 8
SQUARE_HEIGHT = BOARD_HEIGHT // 8

CAPTURE_HEIGHT = SQUARE_HEIGHT * 8
CAPTURE_WIDTH = SQUARE_WIDTH * 2

# Set the colors for the chessboard squares
# LIGHT_SQUARE_COLOR = arcade.color.ALMOND
# DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN
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
MOVE_SOUND = "sounds/make_move.wav"
CAPTURE_SOUND = "sounds/capture.wav"
PROMOTE_SOUND = "sounds/promote.wav"
CASTLE_SOUND = "sounds/castle.wav" # TODO: Add sound to castle function

# p = pieces.Piece
white_allegiance = "White"
black_allegiance = "Black"

theme_manager = ManageTheme("default")
game_manager = ManageGame("_")
sound_manager = ManageSound(1)

BULLET_SPEED = 5

EXPLOSION_TEXTURE_COUNT = 60
class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()


class Board(arcade.View):
    def __init__(self, versus):
        super().__init__()
        self.versus = versus
        self.manager = arcade.gui.UIManager()

        # Add a variable to track whose turn it is
        self.current_turn = white_allegiance  # Start with white's turn

        self.valid_moves = []
        self.capture_moves = []
        self.captures = []
        self.white_capture_board = np.array([[None for _ in range(2)] for _ in range(8)])
        self.black_capture_board = np.array([[None for _ in range(2)] for _ in range(8)])

        arcade.set_background_color(arcade.color.WHITE)
        self.board = np.array([[None for _ in range(COLS)] for _ in range(ROWS)])
        self.prev_board = copy.copy(self.board)
        self.selected_piece = None
        self.computer_piece = None
        self.captured_piece = None
        self.selected_row = None
        self.selected_col = None

        self.explosions_list = arcade.SpriteList()
        self.explosion_texture_list = []

        # Setup explosions
        self.setup_explosions()

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
        self.theme = theme_manager.theme
        self.bg_color, self.black_capture_bg, self.white_capture_bg = theme_manager.get_background(self.theme)

        arcade.set_background_color(self.bg_color)

        self.settings_png = arcade.load_texture("pieces_png/settings_cog.png")
        self.tutorial_png = arcade.load_texture("pieces_png/Black_question_mark.png")
        self.exit_png = arcade.load_texture("pieces_png/letter_x.png")

        settings_button = arcade.gui.UITextureButton(x=SCREEN_WIDTH - (SQUARE_WIDTH // 2) - 60,
                                                     y=(SCREEN_HEIGHT - SQUARE_HEIGHT // 2) - 60,
                                                     width=60,
                                                     height=60,
                                                     texture=self.settings_png)

        tutorial_button = arcade.gui.UITextureButton(x=(SCREEN_WIDTH - (SQUARE_WIDTH // 2) * 3) - 60,
                                                     y=(SCREEN_HEIGHT - SQUARE_HEIGHT // 2) - 60,
                                                     width=60,
                                                     height=60,
                                                     texture=self.tutorial_png)

        @settings_button.event("on_click")
        def on_click_switch_button(event):
            # game_view = SettingsView(self.theme_manager.theme)
            # self.window.show_view(game_view)
            sound_manager.play_button_sound()
            settings_menu = s.SettingsMenu(
                "Settings",
                "Volume",
                theme_manager,
                sound_manager
            )
            self.manager.add(
                settings_menu
            )
        @tutorial_button.event("on_click")
        def on_click_switch_button(event):
            sound_manager.play_button_sound()
            tutorial_menu = t.SubMenu(
                "Tutorial Menu"
            )
            self.manager.add(
                tutorial_menu
            )

        self.manager.add(tutorial_button)
        self.manager.add(settings_button)

        # Bools to avoid loops
        self.promotion_triggered = False
        self.castle_triggered = False

    def setup_explosions(self):
        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

    def on_show(self):
        arcade.set_background_color(self.bg_color)
        self.manager.enable()
        # self.chess_piece.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()



    def on_update(self, delta_time):
        self.explosions_list.update()

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

                """ Check for pawn promotion """
                if not self.promotion_triggered:
                    # Allows pawn to move to position before promoting to queen
                    if self.selected_piece.promotable():
                        self.promote_pawn_to_queen(self.selected_piece.current_row, self.selected_piece.current_col)
                        self.promotion_triggered = True
                    elif self.computer_piece is not None and self.computer_piece.promotable():
                        self.promote_pawn_to_queen(self.computer_piece.current_row, self.computer_piece.current_col)
                        self.promotion_triggered = True

                """ Check if castle move """
                if not self.castle_triggered:
                    castle = self.selected_piece.castle()

                    if castle is not None:
                        print("CASTLE1")
                        print(f"curr: {self.selected_piece.current_row} col: {self.selected_piece.current_col}")
                        print(f"selected: {self.selected_row} col: {self.selected_col}")
                        for cas_row, cas_col, rook_col, new_rook_col in castle:
                            if cas_row == self.selected_row and cas_col == self.selected_col:
                                print("CASTLE...")
                                # TODO: Play sound
                                # self.castle_rook(cas_row, rook_col, new_rook_col)
                                # self.castle_triggered = True

        if game_manager.get_game_type() == "Replay":
            game_manager.set_game_type("_")
            self.__init__(self.versus)
        elif game_manager.get_game_type() == "Main_Menu":
            game_manager.set_game_type("_")
            game_view = menu.MenuView(theme_manager.theme, sound_manager.get_volume())
            self.window.show_view(game_view)



    def on_draw(self):
        self.clear()
        arcade.start_render()

        self.theme = theme_manager.theme
        self.bg_color, self.black_capture_bg, self.white_capture_bg = theme_manager.get_background(self.theme)
        self.light_square_color, self.dark_square_color = theme_manager.get_theme(self.theme)

        if self.theme == "midnight":
            background = arcade.load_texture("pieces_png/midnight1.jpg")
            background.draw_sized(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2,
                                  width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

        elif self.theme == "ocean":
            background = arcade.load_texture("pieces_png/ocean.jpg")
            background.draw_sized(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2,
                                  width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        else:
            arcade.set_background_color(self.bg_color)

        # Make even squares
        square_width = (BOARD_WIDTH - 200) // COLS
        square_height = BOARD_HEIGHT // ROWS

        arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 8 + 10,
                                      height=square_height * 8 + 10,
                                      color=self.light_square_color,
                                      border_width=2)

        arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 8 + 20,
                                      height=square_height * 8 + 20,
                                      color=self.light_square_color,
                                      border_width=3)

        # TODO Clean this up

        #BLACK CAPTURE ZONE
        arcade.draw_rectangle_outline(center_x=(2 * square_width) + (SCREEN_WIDTH / 12),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 2 + 10,
                                      height=square_height * 8 + 10,
                                      color=self.light_square_color,
                                      border_width=2)

        arcade.draw_rectangle_outline(center_x=(2 * square_width) + (SCREEN_WIDTH / 12),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 2 + 20,
                                      height=square_height * 8 + 20,
                                      color=self.light_square_color,
                                      border_width=2)

        arcade.draw_rectangle_filled(center_x=(2 * square_width) + (SCREEN_WIDTH / 12),
                                     center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                     width=square_width * 2,
                                     height=square_height * 8,
                                     color=self.black_capture_bg)

        #WHITE CAPTURE ZONE
        arcade.draw_rectangle_outline(center_x=SCREEN_WIDTH - ((2 * square_width) + (SCREEN_WIDTH / 12)),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 2 + 10,
                                      height=square_height * 8 + 10,
                                      color=self.light_square_color,
                                      border_width=2)

        arcade.draw_rectangle_outline(center_x=SCREEN_WIDTH - ((2 * square_width) + (SCREEN_WIDTH / 12)),
                                      center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                      width=square_width * 2 + 20,
                                      height=square_height * 8 + 20,
                                      color=self.light_square_color,
                                      border_width=2)

        arcade.draw_rectangle_filled(center_x=SCREEN_WIDTH - ((2 * square_width) + (SCREEN_WIDTH / 12)),
                                     center_y=(4 * square_height) + (SCREEN_HEIGHT // 6),
                                     width=square_width * 2,
                                     height=square_height * 8,
                                     color=self.white_capture_bg)

        for row in range(ROWS):
            for col in range(COLS):
                x = (col * square_width) + (SCREEN_WIDTH / 3.25)
                y = (row * square_height) + (SCREEN_HEIGHT // 6)

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

        for row in range(8):
            for col in range(2):
                # Draw the piece if it exists at this position
                white_piece = self.white_capture_board[row][col]
                black_piece = self.black_capture_board[row][col]

                if isinstance(white_piece, p.Piece):
                    white_piece.draw()
                if isinstance(black_piece, p.Piece):
                    black_piece.draw()

        # Draw the timers for white and black players
        self.draw_timer(self.WHITE_TIME, "White")
        self.draw_timer(self.BLACK_TIME, "Black")



        self.manager.draw()

        self.explosions_list.draw()

    def draw_timer(self, remaining_time, player):

        square_width = (BOARD_WIDTH - 200) // COLS
        square_height = BOARD_HEIGHT // ROWS

        # Whites time and Title
        if player == "White":
            arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                          center_y=(SCREEN_HEIGHT // 12),
                                          width=square_width * 4 + 10,
                                          height=square_height * 0.5 + 10,
                                          color=self.light_square_color,
                                          border_width=2)

            arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                          center_y=(SCREEN_HEIGHT // 12),
                                          width=square_width * 4 + 20,
                                          height=square_height * 0.5 + 20,
                                          color=self.light_square_color,
                                          border_width=3)

            arcade.draw_text(text=f"{remaining_time.seconds // 60:02d}:{remaining_time.seconds % 60:02d}",
                             start_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                             start_y=(SCREEN_HEIGHT // 14.5),
                             color=self.light_square_color,
                             font_size=25,
                             font_name="Kenney Blocks",
                             anchor_x="center"
                             )
        else:
            # Blacks timer and Title
            arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                          center_y=SCREEN_HEIGHT - (SCREEN_HEIGHT // 14),
                                          width=square_width * 4 + 10,
                                          height=square_height * 0.5 + 10,
                                          color=self.light_square_color,
                                          border_width=2)

            arcade.draw_rectangle_outline(center_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                                          center_y=SCREEN_HEIGHT - (SCREEN_HEIGHT // 14),
                                          width=square_width * 4 + 20,
                                          height=square_height * 0.5 + 20,
                                          color=self.light_square_color,
                                          border_width=3)

            arcade.draw_text(text=f"{remaining_time.seconds // 60:02d}:{remaining_time.seconds % 60:02d}",
                             start_x=((4 * square_width) + (SCREEN_WIDTH / 3.25)),
                             start_y=SCREEN_HEIGHT - (SCREEN_HEIGHT / 11.5),
                             color=self.light_square_color,
                             font_size=25,
                             font_name="Kenney Blocks",
                             anchor_x="center"
                             )

    def on_mouse_press(self, x, y, button, modifiers):
        global current_turn_start

        if self.selected_piece is not None and self.selected_piece.is_moving:
            # Piece is still moving, do not allow any interaction
            return

        # Start the timer when a player makes a move
        self.current_turn_start = datetime.now()

        # Square boundaries
        square_width = (BOARD_WIDTH - 200) // COLS
        square_height = BOARD_HEIGHT // ROWS

        # Map to corresponding column and row
        if x < (SCREEN_WIDTH / 3.25):
            return

        col = int((x - (SCREEN_WIDTH / 3.25)) // square_width)
        row = int((y - (SCREEN_HEIGHT // 6)) // square_height)


        # If a piece is selected
        if any(self.selected[r][c] for r in range(ROWS) for c in range(COLS)):
            # If the clicked spot is a valid move
            if (row, col) in self.valid_moves:
                # Move the selected piece to the clicked spot
                self.move_piece(row, col)
                sound_manager.play_move_sound()

            # If the clicked spot is a capture move
            elif (row, col) in self.capture_moves:
                # Record capture in list
                self.make_capture(self.board[row][col])
                self.captured_piece = self.board[row][col]

                # Move the selected piece to the clicked spot
                self.move_piece(row, col)

                # Make an explosion
                explosion = Explosion(self.explosion_texture_list)

                x = (col * SQUARE_WIDTH) + (SCREEN_WIDTH / 3.25) + SQUARE_WIDTH // 2
                y = (row * SQUARE_HEIGHT) + (SCREEN_HEIGHT // 6) + SQUARE_HEIGHT // 2

                # Move it to the location of the coin
                explosion.center_x = x
                explosion.center_y = y

                # Call update() because it sets which image we start on
                explosion.update()

                # Add to a list of sprites that are explosions
                self.explosions_list.append(explosion)
                # arcade.play_sound(audio, 1.0, -1, False)

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
                    self.valid_moves, self.capture_moves, self.attack_moves = piece.available_moves(False)

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
                    self.valid_moves, self.capture_moves, self.attack_moves = piece.available_moves(False)
                    # print(self.valid_moves, self.capture_moves)

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

        # Rooks
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

        # Bishops
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

        # Rooks
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

        # pawn = p.Pawn(allegiance, self.board, [5, 5])
        # self.add_to_board(pawn, [5, 5])

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
        piece = self.board[self.selected_row][self.selected_col]
        print(f"Piece before move {piece} and selected {self.selected_piece}")

        x = (col * SQUARE_WIDTH) + (SCREEN_WIDTH / 3.25)
        y = (row * SQUARE_HEIGHT) + (SCREEN_HEIGHT // 6)

        self.selected_piece.on_click(x, y)
        print(self.selected_piece)

        # Deselect the piece and switch turn after animation is complete
        piece.move([row, col])

        """Check if castle move"""
        castle = self.selected_piece.castle()
        if castle is not None:
            print(f"Piece during move {self.selected_piece}")

            for cas_row, cas_col, rook_col, new_rook_col in castle:
                if cas_row == row and cas_col == col:
                    print("CASTLE HAPPENING....")
                    # Move the King
                    # self.selected_piece.on_click(col * SQUARE_WIDTH - 37, row * SQUARE_HEIGHT - 35)
                    # self.selected_piece.move([row, col])
                    print(f"Piece during move {self.selected_piece}")
                    # self.board[self.selected_row][self.selected_col] = None
                    # self.board[row][col] = piece

                    print("CASTLE MOVE")
                    self.deselect_all()
                    self.selected_piece = self.board[cas_row][rook_col]
                    self.selected_piece.on_click(new_rook_col * SQUARE_WIDTH - 37, cas_row * SQUARE_HEIGHT - 35)
                    self.selected_piece.move([cas_row, new_rook_col])
                    print(f"Piece during rook move {self.selected_piece}")
                    self.board[cas_row][rook_col] = None
                    self.board[cas_row][new_rook_col] = self.selected_piece

                    break

        """ Check if move is en passant """
        cap = self.selected_piece.en_passant([row, col])
        if cap is not None:
            # self.captures.append(self.board[cap[0]][cap[1]])
            # self.imprison_piece(self.board[cap[0]][cap[1]])
            self.make_capture(self.board[cap[0]][cap[1]])
            self.captured_piece = self.board[row][col]
            self.board[cap[0]][cap[1]] = None

        # Update board position
        self.board[self.selected_row][self.selected_col] = None
        self.board[row][col] = piece

        # Wait for the animation to finish
        # time.sleep(1)  # Adjust the delay as needed

        """ Change to queen if pawn promotable """
        # TODO: Save me
        # if self.selected_piece.promotable():
        #     self.promote_pawn_to_queen(row, col)

        self.deselect_all()

        print("============= Whites Turn ===========")
        self.print_board()

        if piece.allegiance == 'White':
            self.check_game_over('Black')
        else:
            self.check_game_over('White')
        # self.print_capture()
        self.switch_turn()

    def promote_pawn_to_queen(self, row, col):
        sound_manager.play_promote_sound()

        piece = p.Queen(self.selected_piece.allegiance, self.board, [row, col])
        self.board[row][col] = piece

        #self.deselect_all()

    def castle_rook(self, row, col, new_col):
        # Need to pass in index chosen (so where king moved to) minus or plus one
        # So pass in cas_row and rook_col
        print("CASTLE ROOK FUNC")
        rook = self.board[row][col]
        rook.on_click(new_col * SQUARE_WIDTH - 37, row * SQUARE_HEIGHT - 35)
        rook.move([row, new_col])
        self.board[row][new_col] = rook

    def switch_turn(self):
        self.promotion_triggered = False
        self.castle_triggered = False
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

            computer_piece, coords = self.computer.make_best_move(2)

            print(f"Move {computer_piece} to {coords}")

            self.computer_piece = computer_piece
            x = (coords[1] * SQUARE_WIDTH) + (SCREEN_WIDTH / 3.25)
            y = (coords[0] * SQUARE_HEIGHT) + (SCREEN_HEIGHT // 6)

            self.computer_piece.on_click(x, y)

            print("============= Blacks Turn ============")
            self.print_board()
            # self.print_capture()
            print("CAPTURES")
            self.print_capture()
            if computer_piece.allegiance == 'White':
                self.check_game_over('Black')
            else:
                self.check_game_over('White')
            self.switch_turn()

    def make_capture(self, piece):
        # allegiance = piece.allegiance
        offset = SQUARE_WIDTH

        sound_manager.play_capture_sound()

        for row in range(8):
            for col in range(2):
                if piece.allegiance == "White":
                    if self.white_capture_board[row][col] is None:
                        x = col * SQUARE_WIDTH + (SCREEN_WIDTH / 12) + offset
                        y = row * SQUARE_HEIGHT + (SCREEN_HEIGHT // 6)
                        self.white_capture_board[row][col] = piece
                        piece.update_target(x, y)
                        self.captured_piece = piece
                        return
                elif piece.allegiance == "Black":
                    if self.black_capture_board[row][col] is None:
                        x = SCREEN_WIDTH - (col * SQUARE_WIDTH + (SCREEN_WIDTH / 12) + (2 * offset))
                        y = row * SQUARE_HEIGHT + (SCREEN_HEIGHT // 6)
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
            moves, caps, attacks = i.available_moves(False)
            # record if each piece has any moves available
            for j in moves:
                all_moves.append(j)

            for k in caps:
                all_moves.append(k)

        # print('MOVES: ', all_moves)
        print('CHECK: ', king_in_check)

        # if there are no possible moves and the king is in check
        if all_moves == [] and king_in_check:
            if pieces[0].allegiance == 'White':
                win_menu = w.WinLoseMenu(theme_manager, "black", game_manager)
                self.manager.add(win_menu)
            else:
                win_menu = w.WinLoseMenu(theme_manager, "white", game_manager)
                self.manager.add(win_menu)
        elif all_moves == [] and not king_in_check:
            win_menu = w.WinLoseMenu(theme_manager, "draw", game_manager)
            self.manager.add(win_menu)




        # print("PIECES")
        # print(pieces)