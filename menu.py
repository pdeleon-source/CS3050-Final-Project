# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change

"""
Create a display Menu, that starts up the chess game
- Give user two options
- Computer V Computer: normal game
- Player V Player: some stuff
- Later we need to implement Puzzle and Tutorial buttons
"""

import arcade
import board
import sys
import time

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

# Define default colors
BG_COLOR = arcade.color.BRUNSWICK_GREEN

TEXT_COLOR = arcade.color.BLACK
LIGHT_SQUARE_COLOR = arcade.color.ALMOND
DARK_SQUARE_COLOR = arcade.color.SADDLE_BROWN

LIGHT_SQUARE_COLOR_PINK = arcade.color.CAMEO_PINK
DARK_SQUARE_COLOR_PINK = arcade.color.CHINA_PINK
BG_COLOR_PINK = arcade.color.WHITE

DEFAULT_THEME = [arcade.color.ALMOND, arcade.color.SADDLE_BROWN, arcade.color.BRUNSWICK_GREEN]
PINK_THEME = [arcade.color.CAMEO_PINK, arcade.color.CHINA_PINK, arcade.color.WHITE]

BUTTON_COLOR = arcade.color.WHITE

# Define sound effects - must be .wav :(
BUTTON_SOUND = "sounds/doink.wav"
MENU_SOUND = "sounds/bob.wav"


class Button:
    def __init__(self, x, y, width, height, volume):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # self.color = arcade.color.WHITE
        self.hover_color = arcade.color.LIGHT_GRAY
        self.clicked_color = arcade.color.GREEN
        self.is_hovered = False
        self.is_clicked = False
        # Volume of sound
        self.volume = volume

    def draw(self, text, color):
        if self.is_clicked:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.clicked_color)
        elif self.is_hovered:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.hover_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        # arcade.draw_text(text, self.x - self.width // 10, self.y - self.height // 10, arcade.color.BLACK, size)
        arcade.draw_text(text, self.x - len(text) * 5, self.y - self.height // 10, arcade.color.BLACK, 16)

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovered = (self.x - self.width / 2 < x < self.x + self.width / 2 and
                           self.y - self.height / 2 < y < self.y + self.height / 2)

    def on_mouse_press(self, x, y, button, modifiers):

        if self.is_hovered:
            # Play sound
            audio = arcade.load_sound(BUTTON_SOUND, False)
            arcade.play_sound(audio, self.volume, -1, False)

            self.is_clicked = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.is_clicked = False

    def set_volume(self, lvl):
        self.volume = lvl


class MenuView(arcade.View):
    def __init__(self, theme, volume):
        super().__init__()
        self.logo = arcade.load_texture("pieces_png/chess_logo.png")
        self.play_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 25, 200, 40, volume)  # Center - 40, Height was 60
        self.tutorial_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 70, 200, 40, volume)  # Center - 110, Height was 60
        self.settings_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 115, 200, 40, volume)
        self.quit_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 160, 200, 40, volume)
        self.game_view = None  # Placeholder for the game view instance

        # Create theme object and set theme
        self.theme_manager = ManageTheme(theme)
        # self.theme_manager.set_theme(theme)
        self.volume = volume

    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        arcade.start_render()

        # Make even squares

        ROWS = SCREEN_WIDTH // SQUARE_WIDTH
        COLS = SCREEN_HEIGHT // SQUARE_HEIGHT

        light_square_color, dark_square_color = self.theme_manager.get_colors()

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        # Draw the logo stuff
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT, width=700, height=580)  # Was w=600h=500
        self.play_button.draw("Play", BUTTON_COLOR)
        self.tutorial_button.draw("Tutorials", BUTTON_COLOR)
        self.settings_button.draw("Settings", BUTTON_COLOR)
        self.quit_button.draw("Quit", BUTTON_COLOR)

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
        self.settings_button.on_mouse_motion(x, y, dx, dy)
        self.quit_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.play_button.on_mouse_press(x, y, button, modifiers)
        self.tutorial_button.on_mouse_press(x, y, button, modifiers)
        self.settings_button.on_mouse_press(x, y, button, modifiers)
        self.quit_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.play_button.on_mouse_release(x, y, button, modifiers)
        self.tutorial_button.on_mouse_release(x, y, button, modifiers)
        self.settings_button.on_mouse_release(x, y, button, modifiers)
        self.quit_button.on_mouse_release(x, y, button, modifiers)

    def update(self, delta_time):
        if self.play_button.is_clicked:
            game_view = GameView(self.theme_manager, self.volume)
            self.window.show_view(game_view)
        if self.settings_button.is_clicked:
            game_view = SettingsView(self.theme_manager, self.volume)
            self.window.show_view(game_view)
        # if self.tutorial_button.is_clicked:
        if self.quit_button.is_clicked:
            # Sleep so sound effect can play :)
            time.sleep(.15)
            sys.exit()


# Testing
class GameView(arcade.View):
    def __init__(self, theme, volume):
        super().__init__()
        self.logo = arcade.load_texture("pieces_png/game_mode.png")
        self.player_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 40, 250, 60, volume)
        self.computer_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 110, 250, 60, volume)
        self.return_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 180, 250, 60, volume)
        # self.chess_piece = arcade.Sprite("pieces_png/white-pawn.png", center_x=SCREEN_WIDTH // 2,
        # s center_y=SCREEN_HEIGHT // 2)

        self.theme_manager = theme
        self.volume = volume

    def on_mouse_motion(self, x, y, dx, dy):
        self.player_button.on_mouse_motion(x, y, dx, dy)
        self.computer_button.on_mouse_motion(x, y, dx, dy)
        self.return_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.player_button.on_mouse_press(x, y, button, modifiers)
        self.computer_button.on_mouse_press(x, y, button, modifiers)
        self.return_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.player_button.on_mouse_press(x, y, button, modifiers)
        self.computer_button.on_mouse_release(x, y, button, modifiers)
        self.return_button.on_mouse_release(x, y, button, modifiers)

        if self.player_button.is_clicked:
            self.game_view = GameView(self.theme_manager, self.volume)  # Create an instance of the game view
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

        light_square_color, dark_square_color = self.theme_manager.get_colors()

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        # Draw the logo stuff
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT + 120, width=600, height=200)
        self.player_button.draw("Player vs Player", BUTTON_COLOR)
        self.computer_button.draw("Player vs Computer", BUTTON_COLOR)
        self.return_button.draw("Go Back", BUTTON_COLOR)

    def update(self, delta_time):
        if self.player_button.is_clicked:
            game_view = board.Board("player", self.theme_manager.theme, self.volume)
            self.window.show_view(game_view)
        if self.computer_button.is_clicked:
            game_view = board.Board("computer", self.theme_manager.theme, self.volume)
            self.window.show_view(game_view)
        if self.return_button.is_clicked:
            game_view = MenuView(self.theme_manager.theme, self.volume)
            self.window.show_view(game_view)


class SettingsView(arcade.View):
    def __init__(self, theme, volume):
        super().__init__()
        self.logo = arcade.load_texture("pieces_png/settings_logo.png")
        self.sound_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 40, 250, 60, volume)
        self.theme_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 110, 250, 60, volume)
        self.return_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 180, 250, 60, volume)

        # self.chess_piece = arcade.Sprite("pieces_png/white-pawn.png", center_x=SCREEN_WIDTH // 2,
        # s center_y=SCREEN_HEIGHT // 2)
        self.theme_manager = theme
        self.volume = volume
        if self.volume == 1.0:
            self.button_text = "Sound Off"
        else:
            self.button_text = "Sound On"

    def on_mouse_motion(self, x, y, dx, dy):
        self.sound_button.on_mouse_motion(x, y, dx, dy)
        self.theme_button.on_mouse_motion(x, y, dx, dy)
        self.return_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.sound_button.on_mouse_press(x, y, button, modifiers)
        self.theme_button.on_mouse_press(x, y, button, modifiers)
        self.return_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.sound_button.on_mouse_release(x, y, button, modifiers)
        self.theme_button.on_mouse_release(x, y, button, modifiers)
        self.return_button.on_mouse_release(x, y, button, modifiers)

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

        light_square_color, dark_square_color = self.theme_manager.get_colors()

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        # Draw the logo stuff
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT + 120, width=600, height=200)

        self.theme_button.draw("Change Theme", BUTTON_COLOR)
        self.sound_button.draw(self.button_text, BUTTON_COLOR)
        self.return_button.draw("Go Back", BUTTON_COLOR)

    def update(self, delta_time):
        if self.sound_button.is_clicked and self.volume == 0.0:
            game_view = SettingsView(self.theme_manager, 1.0)
            self.window.show_view(game_view)
        if self.sound_button.is_clicked and self.volume == 1.0:
            game_view = SettingsView(self.theme_manager, 0.0)
            self.window.show_view(game_view)

        if self.theme_button.is_clicked:
            print("Theme")
            game_view = ThemeView(self.theme_manager, self.volume)
            self.window.show_view(game_view)
        if self.return_button.is_clicked:
            # NOTE: Menu is the only one which takes in a string for theme
            game_view = MenuView(self.theme_manager.theme, self.volume)
            self.window.show_view(game_view)


class ThemeView(arcade.View):
    def __init__(self, theme, volume):
        super().__init__()

        # Theme buttons
        self.default_button = Button(CENTER_WIDTH - 200, CENTER_HEIGHT + 150, 200, 200, volume)
        self.pink_button = Button(CENTER_WIDTH + 200, CENTER_HEIGHT + 150, 200, 200, volume)
        self.ocean_button = Button(CENTER_WIDTH - 200, CENTER_HEIGHT - 100, 200, 200, volume)
        self.midnight_button = Button(CENTER_WIDTH + 200, CENTER_HEIGHT - 100, 200, 200, volume)

        self.return_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 250, 250, 60, volume)

        # Initialize theme management object
        self.theme_manager = theme
        self.volume = volume

    def on_draw(self):
        arcade.start_render()

        # Make even squares

        ROWS = SCREEN_WIDTH // SQUARE_WIDTH
        COLS = SCREEN_HEIGHT // SQUARE_HEIGHT

        light_square_color, dark_square_color = self.theme_manager.get_colors()

        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)
        self.default_button.draw("Default Theme", arcade.color.ALMOND)
        self.pink_button.draw("Pink Theme", arcade.color.PINK)
        self.ocean_button.draw("Ocean Theme", arcade.color.OCEAN_BOAT_BLUE)
        self.midnight_button.draw("Midnight Theme", arcade.color.MIDNIGHT_BLUE)

        self.return_button.draw("Go Back", BUTTON_COLOR)

    def on_mouse_motion(self, x, y, dx, dy):
        self.default_button.on_mouse_motion(x, y, dx, dy)
        self.pink_button.on_mouse_motion(x, y, dx, dy)
        self.ocean_button.on_mouse_motion(x, y, dx, dy)
        self.midnight_button.on_mouse_motion(x, y, dx, dy)
        self.return_button.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, x, y, button, modifiers):
        self.default_button.on_mouse_press(x, y, button, modifiers)
        self.pink_button.on_mouse_press(x, y, button, modifiers)
        self.ocean_button.on_mouse_press(x, y, button, modifiers)
        self.midnight_button.on_mouse_press(x, y, button, modifiers)
        self.return_button.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.default_button.on_mouse_release(x, y, button, modifiers)
        self.pink_button.on_mouse_release(x, y, button, modifiers)
        self.ocean_button.on_mouse_release(x, y, button, modifiers)
        self.midnight_button.on_mouse_release(x, y, button, modifiers)
        self.return_button.on_mouse_press(x, y, button, modifiers)

        # def on_show(self):
        #     arcade.set_background_color(arcade.color.WHITE)
        #     self.chess_piece.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def update(self, delta_time):
        if self.default_button.is_clicked:
            self.theme_manager.set_theme("default")
        if self.pink_button.is_clicked:
            self.theme_manager.set_theme("pink")
        if self.ocean_button.is_clicked:
            self.theme_manager.set_theme("ocean")
        if self.midnight_button.is_clicked:
            self.theme_manager.set_theme("midnight")

        if self.return_button.is_clicked:
            game_view = SettingsView(self.theme_manager, self.volume)
            self.window.show_view(game_view)


class ManageTheme:
    def __init__(self, theme):
        # Default theme values
        # self.theme = theme
        # self.light_square_color = arcade.color.ALMOND
        # self.dark_square_color = arcade.color.SADDLE_BROWN
        self.set_theme(theme)

    def get_colors(self):
        return self.light_square_color, self.dark_square_color

    def set_theme(self, theme):
        if theme == "midnight":
            self.light_square_color = arcade.color.QUEEN_BLUE
            self.dark_square_color = arcade.color.DARK_MIDNIGHT_BLUE
            # self.bg_color = arcade.color.BRUNSWICK_GREEN
        elif theme == "pink":
            self.light_square_color = arcade.color.CAMEO_PINK
            self.dark_square_color = arcade.color.CHINA_PINK
            # self.bg_color = arcade.color.WHITE
        elif theme == "ocean":
            self.light_square_color = arcade.color.PALE_ROBIN_EGG_BLUE
            self.dark_square_color = arcade.color.DARK_CYAN
            # self.bg_color = arcade.color.WHITE
        else:  # Default colors
            self.light_square_color = arcade.color.ALMOND
            self.dark_square_color = arcade.color.SADDLE_BROWN
            # self.bg_color = arcade.color.BRUNSWICK_GREEN

        self.theme = theme



def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView("default", 1.0)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
