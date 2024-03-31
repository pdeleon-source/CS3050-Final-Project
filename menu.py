# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change

"""
Create a display Menu, that starts up the chess game
- Give user two options
- Computer V Computer: normal game
- Player V Player: some stuff
- Later we need to implement Puzzle and Turtorial buttons
"""

import arcade
import board


# Define screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Chess Game Intro"
CENTER_WIDTH = SCREEN_WIDTH // 2
CENTER_HEIGHT = SCREEN_HEIGHT // 2

# Set the dimensions of the chessboard
ROWS = 8
COLS = 8
SQUARE_WIDTH = SCREEN_WIDTH // 8
SQUARE_HEIGHT = SCREEN_HEIGHT // 8

# Define colors
BG_COLOR = arcade.color.LIGHT_BLUE
TEXT_COLOR = arcade.color.BLACK
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN

class Button:
    #SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size(
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = arcade.color.WHITE
        self.hover_color = arcade.color.LIGHT_GRAY
        self.clicked_color = arcade.color.GREEN
        self.is_hovered = False
        self.is_clicked = False

    def draw(self, text, size):
        if self.is_clicked:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.clicked_color)
        elif self.is_hovered:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.hover_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)
        #arcade.draw_text(text, self.x - self.width // 10, self.y - self.height // 10, arcade.color.BLACK, size)
        arcade.draw_text(text, self.x - len(text) * 5, self.y - self.height // 10, arcade.color.BLACK, 16)

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovered = (self.x - self.width / 2 < x < self.x + self.width / 2 and
                           self.y - self.height / 2 < y < self.y + self.height / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_hovered:
            self.is_clicked = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.is_clicked = False

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.logo = arcade.load_texture("pieces_png/chess_logo.png")
        self.play_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 40, 200, 60)
        self.tutorial_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 110, 200, 60)
        self.game_view = None  # Placeholder for the game view instance

    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Make even squares

        ROWS = SCREEN_WIDTH // SQUARE_WIDTH
        COLS = SCREEN_HEIGHT // SQUARE_HEIGHT

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        # Draw the logo stuff
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT, width=600, height=500)
        self.play_button.draw("Play", 16)
        self.tutorial_button.draw("Quit", 16)

    # def on_key_press(self, key, modifiers):
    #     if key == arcade.key.KEY_1:
    #         # Start game against another player
    #         game_view = GameView()
    #         self.window.show_view(game_view)
    #     elif key == arcade.key.KEY_2:
    #         # Start game against the computer
    #         computer_game_view = ComputerGameView()
    #         self.window.show_view(computer_game_view)

    def on_mouse_motion(self, x, y, dx, dy):
        self.play_button.on_mouse_motion(x, y, dx, dy)
        self.tutorial_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.play_button.on_mouse_press(x, y, button, modifiers)
        self.tutorial_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.play_button.on_mouse_press(x, y, button, modifiers)
        self.tutorial_button.on_mouse_release(x, y, button, modifiers)


    def update(self, delta_time):
        if self.play_button.is_clicked:
            game_view = GameView()
            self.window.show_view(game_view)
        # if self.tutorial_button.is_clicked:
        #



# Testing
class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.logo = arcade.load_texture("pieces_png/game_mode.png")
        self.player_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 40, 250, 60)
        self.computer_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 110, 250, 60)

        # self.chess_piece = arcade.Sprite("pieces_png/white-pawn.png", center_x=SCREEN_WIDTH // 2,
                                        #s center_y=SCREEN_HEIGHT // 2)

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_button.on_mouse_motion(x, y, dx, dy)
        self.computer_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.player_button.on_mouse_press(x, y, button, modifiers)
        self.computer_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.player_button.on_mouse_press(x, y, button, modifiers)
        self.computer_button.on_mouse_release(x, y, button, modifiers)
        if self.player_button.is_clicked:
            self.game_view = GameView()  # Create an instance of the game view
            self.window.show_view(self.game_view)  # Show the game view
        elif self.computer_button.is_clicked:
            if self.game_view:
                self.window.show_view(self)

    # def on_show(self):
    #     arcade.set_background_color(arcade.color.WHITE)
    #     self.chess_piece.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Make even squares

        ROWS = SCREEN_WIDTH // SQUARE_WIDTH
        COLS = SCREEN_HEIGHT // SQUARE_HEIGHT

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = LIGHT_SQUARE_COLOR
                else:
                    color = DARK_SQUARE_COLOR

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        # Draw the logo stuff
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT + 120, width=600, height=200)
        self.player_button.draw("Player vs Player", 12)
        self.computer_button.draw("Player vs Computer", 12)
    def update(self, delta_time):
        if self.player_button.is_clicked:
            game_view = board.Board("player")
            self.window.show_view(game_view)
        if self.computer_button.is_clicked:
            game_view = board.Board("computer")
            self.window.show_view(game_view)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()




