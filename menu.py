# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change

"""
Create a display Menu, that starts up the chess game
- Give user two options
- Computer V Computer: normal game
- Player V Player: some stuff
- Later we need to implement Puzzle and Tutorial buttons
"""

# TODO: Replace Button Class, for arcade 2.7.1.dev11 mmmmm make a THING

import arcade
import board
import sys
import time
import tutorial as t
import setting as s
import arcade.gui
from theme_manager import ManageTheme

import arcade.gui.widgets
import arcade.gui.widgets
from arcade.experimental.uistyle import UIFlatButtonStyle

# Define screen dimensions
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

SCREEN_TITLE = "Chess Game Intro"
CENTER_WIDTH = SCREEN_WIDTH // 2
CENTER_HEIGHT = SCREEN_HEIGHT // 2

# Set the dimensions of the chessboard
ROWS = 8
COLS = 8
SQUARE_WIDTH = 800 // 8
SQUARE_HEIGHT = 800 // 8

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

VOLUME = 1

theme_manager = ManageTheme("default")

# Render button
default_style = {
    "normal": UIFlatButtonStyle(
        font_size=12,
        font_name=("calibri", "arial"),
        font_color=arcade.color.BRUNSWICK_GREEN,
        bg=arcade.color.WHITE,
        border=None,
        border_width=0,
    ),
    "hover": UIFlatButtonStyle(
        font_size=12,
        font_name=("calibri", "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.color.BRUNSWICK_GREEN,
        border=None,
        border_width=2,
    ),
    "press": UIFlatButtonStyle(
        font_size=12,
        font_name=("calibri", "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.color.BRUNSWICK_GREEN,
        border=arcade.color.ARMY_GREEN,
        border_width=2,
    ),
    "disabled": UIFlatButtonStyle(
        font_size=12,
        font_name=("calibri", "arial"),
        font_color=arcade.color.WHITE,
        bg=arcade.color.COOL_GREY,
        border=arcade.color.ASH_GREY,
        border_width=2,
    )
}

def set_volume(self, lvl):
    self.volume = lvl


"""
    TODO: Pass in theme manager object instead?
"""


def play_button_sound():
    audio = arcade.load_sound(BUTTON_SOUND, False)
    arcade.play_sound(audio, VOLUME, -1, False)


class MenuView(arcade.View):
    def __init__(self, theme):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        self.logo = arcade.load_texture("pieces_png/chess_logo.png")
        self.settings_png = arcade.load_texture("pieces_png/settings_cog.png")
        self.tutorial_png = arcade.load_texture("pieces_png/Black_question_mark.png")

        play_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 100,
                                              y=CENTER_HEIGHT - 70,
                                              width=200,
                                              height=60,
                                              text="Play",
                                              style=default_style)

        settings_button = arcade.gui.UITextureButton(x=SCREEN_WIDTH - (SQUARE_WIDTH // 2) - 30,
                                                     y=(SCREEN_HEIGHT - SQUARE_HEIGHT // 2) - 60,
                                                     width=60,
                                                     height=60,
                                                     texture=self.settings_png)

        tutorial_button = arcade.gui.UITextureButton(x=(SCREEN_WIDTH - (SQUARE_WIDTH // 2) * 3) - 30,
                                                     y=(SCREEN_HEIGHT - SQUARE_HEIGHT // 2) - 60,
                                                     width=60,
                                                     height=60,
                                                     texture=self.tutorial_png)

        quit_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 100,
                                              y=CENTER_HEIGHT - 160,
                                              width=200,
                                              height=60,
                                              text="Quit",
                                              style=default_style)

        # Initialise the button with an on_click event.
        @play_button.event("on_click")
        def on_click_switch_button(event):
            play_button_sound()
            game_view = GameView(theme_manager.theme)
            self.window.show_view(game_view)

        @quit_button.event("on_click")
        def on_click_switch_button(event):
            play_button_sound()
            time.sleep(.15)
            sys.exit()

        @settings_button.event("on_click")
        def on_click_switch_button(event):
            play_button_sound()
            settings_menu = s.SettingsMenu(
                "Settings",
                "Volume",
                theme_manager
            )
            self.manager.add(
                settings_menu
            )

        @tutorial_button.event("on_click")
        def on_click_switch_button(event):
            play_button_sound()
            tutorial_menu = t.SubMenu(
                "Tutorial Menu",
                "This is a tutorial submenu.",
                "OK"
            )
            self.manager.add(
                tutorial_menu
            )

        # self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        self.manager.add(play_button)
        self.manager.add(tutorial_button)
        self.manager.add(quit_button)
        self.manager.add(settings_button)

        self.game_view = None  # Placeholder for the game view instance

        # Create theme object and set theme

    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        self.clear()
        arcade.start_render()

        # Make even squares

        r = SCREEN_HEIGHT // SQUARE_WIDTH
        c = SCREEN_WIDTH // SQUARE_HEIGHT

        light_square_color, dark_square_color = theme_manager.get_colors()

        for row in range(r + 1):
            for col in range(c + 1):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT, width=700, height=580)  # Was w=600h=500
        self.manager.draw()

    def on_show_view(self):
        """ Render the screen. """
        self.manager.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


# Testing
class GameView(arcade.View):
    def __init__(self, theme):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        self.logo = arcade.load_texture("pieces_png/game_mode.png")

        player_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 250,
                                                y=CENTER_HEIGHT - 60 - 40,
                                                width=250,
                                                height=60,
                                                text="Player vs Player")

        computer_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 250,
                                                  y=CENTER_HEIGHT - 110 - 40,
                                                  width=250,
                                                  height=60,
                                                  text="Player vs Computer")

        return_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 250,
                                                y=CENTER_HEIGHT - 180 - 40,
                                                width=250,
                                                height=60,
                                                text="Return to Main Menu")

        @player_button.event("on_click")
        def on_click_switch_button(event):
            game_view = board.Board("player")
            self.window.show_view(game_view)

        @computer_button.event("on_click")
        def on_click_switch_button(event):
            game_view = board.Board("computer")
            self.window.show_view(game_view)

        @return_button.event("on_click")
        def on_click_switch_button(event):
            game_view = MenuView(theme_manager.theme)
            self.window.show_view(game_view)

        self.manager.add(player_button)
        self.manager.add(computer_button)
        self.manager.add(return_button)

        # self.chess_piece = arcade.Sprite("pieces_png/white-pawn.png", center_x=SCREEN_WIDTH // 2,
        # s center_y=SCREEN_HEIGHT // 2)

        # Create theme manager object and set theme
        theme_manager = ManageTheme(theme)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(BG_COLOR)

        # Enable the UIManager when the view is showm.
        self.manager.enable()

    def on_draw(self):
        self.clear()
        arcade.start_render()

        # Make even squares

        r = SCREEN_HEIGHT // SQUARE_WIDTH
        c = SCREEN_WIDTH // SQUARE_HEIGHT

        light_square_color, dark_square_color = theme_manager.get_colors()

        for row in range(r + 1):
            for col in range(c + 1):
                x = col * SQUARE_WIDTH
                y = row * SQUARE_HEIGHT

                if (row + col) % 2 == 0:
                    color = light_square_color
                else:
                    color = dark_square_color

                arcade.draw_rectangle_filled(x + SQUARE_WIDTH // 2, y + SQUARE_HEIGHT // 2, SQUARE_WIDTH, SQUARE_HEIGHT,
                                             color)

        self.manager.draw()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView("default")
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
