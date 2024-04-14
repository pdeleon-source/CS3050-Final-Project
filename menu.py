"""
This program creates a display menu which provides the user with options. The user may
choose to play against a player or a computer or to view tutorials. The user may also
visit a settings menu to change the theme or toggle sound.
"""

import arcade
import board
import sys
import time
import tutorial as t
import setting as s
import arcade.gui
from theme_manager import ManageTheme
from game_manager import ManageGame

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
PINK_THEME = [arcade.color.CAMEO_PINK, arcade.color.CHINA_PINK, arcade.color.DUST_STORM]
OCEAN_THEME = [arcade.color.PALE_ROBIN_EGG_BLUE, arcade.color.DARK_CYAN, arcade.color.MEDIUM_AQUAMARINE]
MIDNIGHT_THEME = [arcade.color.QUEEN_BLUE, arcade.color.DARK_MIDNIGHT_BLUE, arcade.color.MIDNIGHT_BLUE]
BUTTON_COLOR = arcade.color.WHITE

# Define sound effects - must be .wav :(
BUTTON_SOUND = "sounds/doink.wav"
MENU_SOUND = "sounds/bob.wav"

theme_manager = ManageTheme("default")
game_manager = ManageGame("_")

VOLUME = 1

#Render Button Style
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


class Button:
    """
        Creates an interactive button that the user can click
    """
    def __init__(self, x, y, width, height, volume):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.hover_color = arcade.color.LIGHT_GRAY
        self.clicked_color = arcade.color.GREEN
        self.is_hovered = False
        self.is_clicked = False

        # Volume of sound
        self.volume = volume


    def draw(self, text, color):
        """
            Draws the button to the screen based on its current state
            :param text:
            :param color:
        """
        # Button will look different based on if it is clicked or hovered over
        if self.is_clicked:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.clicked_color)
        elif self.is_hovered:
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.hover_color)
        else:
            arcade.draw_rectangle_filled(self.x, self.y, self.width + 5, self.height + 5, TEXT_COLOR)
            arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)

            # If the button is a theme button
            if color == arcade.color.ALMOND:
                self.draw_checkers(arcade.color.SADDLE_BROWN)
            elif color == arcade.color.CAMEO_PINK:
                self.draw_checkers(arcade.color.CHINA_PINK)
            elif color == arcade.color.QUEEN_BLUE:
                self.draw_checkers(arcade.color.DARK_MIDNIGHT_BLUE)
            elif color == arcade.color.PALE_ROBIN_EGG_BLUE:
                self.draw_checkers(arcade.color.DARK_CYAN)

        # Write text to button
        arcade.draw_text(text, self.x - len(text) * 5, self.y - self.height // 10, TEXT_COLOR, 16)

    def on_mouse_motion(self, x, y, dx, dy):
        # Detect user mouse movement
        self.is_hovered = (self.x - self.width / 2 < x < self.x + self.width / 2 and
                           self.y - self.height / 2 < y < self.y + self.height / 2)

    def on_mouse_press(self, x, y, button, modifiers):
        # Detect user clicks
        if self.is_hovered:
            # Play sound if button clicked
            audio = arcade.load_sound(BUTTON_SOUND, False)
            arcade.play_sound(audio, self.volume, -1, False)

            self.is_clicked = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.is_clicked = False

    def draw_checkers(self, color):
        """
        This method is for theme buttons, which have a special design. Draws
        a checkered pattern of a specified color on the button.
        :param color:
        """
        arcade.draw_rectangle_filled(self.x + self.width // 4, self.y +
                                     self.width // 4, self.width // 2,
                                     self.height // 2, color)
        arcade.draw_rectangle_filled(self.x - self.width // 4, self.y -
                                     self.width // 4, self.width // 2,
                                     self.height // 2, color)

def set_volume(self, lvl):
    self.volume = lvl

def play_button_sound():
    audio = arcade.load_sound(BUTTON_SOUND, False)
    arcade.play_sound(audio, VOLUME, -1, False)


class MenuView(arcade.View):
    """
        The main menu. Has options which allow the user to choose a game mode,
        change settings, and quit the game.
    """
    def __init__(self, theme, volume):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Load game logo
        self.logo = arcade.load_texture("pieces_png/chess_logo.png")
        self.settings_png = arcade.load_texture("pieces_png/settings_cog.png")
        self.tutorial_png = arcade.load_texture("pieces_png/Black_question_mark.png")

        # Create button objects for each option
        # self.play_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 25, 200, 40, volume)  # Center - 40, Height was 60
        # self.tutorial_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 70, 200, 40, volume)  # Center - 110, Height was 60
        # self.settings_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 115, 200, 40, volume)
        # self.quit_button = Button(CENTER_WIDTH, CENTER_HEIGHT - 160, 200, 40, volume)


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
            game_view = GameView(theme_manager)
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
                "Tutorial Menu"
            )
            self.manager.add(
                tutorial_menu
            )

        self.manager.add(play_button)
        self.manager.add(tutorial_button)
        self.manager.add(quit_button)
        self.manager.add(settings_button)

        self.game_view = None  # Placeholder for the game view instance


        self.theme_manager = ManageTheme(theme)
        self.volume = volume

    def on_show(self):
        arcade.set_background_color(BG_COLOR)

    def on_draw(self):
        """
        Draws the menu background as a checkered pattern based on the current theme colors.
        """

        self.clear()
        arcade.start_render()

        # Make even squares

        r = SCREEN_HEIGHT // SQUARE_WIDTH
        c = SCREEN_WIDTH // SQUARE_HEIGHT

        # Get current theme colors
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

        # Draw the logo and buttons
        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT, width=700, height=580)  # Was w=600h=500
        self.manager.draw()

    def on_show_view(self):
        """ Render the screen. """
        self.manager.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

class GameView(arcade.View):
    def __init__(self, theme):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.logo = arcade.load_texture("pieces_png/game_banner.png")
        self.settings_png = arcade.load_texture("pieces_png/settings_cog.png")
        self.tutorial_png = arcade.load_texture("pieces_png/Black_question_mark.png")

        player_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 125,
                                                y=CENTER_HEIGHT,
                                                width=250,
                                                height=60,
                                                text="Player vs Player",
                                                style=default_style)

        computer_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 125,
                                                  y=CENTER_HEIGHT - 70,
                                                  width=250,
                                                  height=60,
                                                  text="Player vs Computer",
                                                  style=default_style)

        return_button = arcade.gui.UIFlatButton(x=CENTER_WIDTH - 125,
                                                y=CENTER_HEIGHT - 140,
                                                width=250,
                                                height=60,
                                                text="Return to Main Menu",
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
                "Tutorial Menu"
            )
            self.manager.add(
                tutorial_menu
            )

        self.manager.add(tutorial_button)
        self.manager.add(settings_button)

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

        theme = theme_manager.theme
        bg_color, black_capture_bg, white_capture_bg = theme_manager.get_background(theme)
        light_square_color, dark_square_color = theme_manager.get_theme(theme)

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

        arcade.draw_rectangle_outline(center_x= CENTER_WIDTH,
                                      center_y=CENTER_HEIGHT - 40,
                                      width=295,
                                      height=260,
                                      color=arcade.color.WHITE,
                                      border_width=4)

        arcade.draw_rectangle_outline(center_x=CENTER_WIDTH,
                                      center_y=CENTER_HEIGHT - 40,
                                      width=275,
                                      height=240,
                                      color=bg_color,
                                      border_width=3)

        arcade.draw_rectangle_filled(center_x=CENTER_WIDTH,
                                     center_y=CENTER_HEIGHT - 40,
                                     width=270,
                                     height=230,
                                     color=black_capture_bg)

        self.logo.draw_sized(center_x=CENTER_WIDTH, center_y=CENTER_HEIGHT + 100, width=700, height=580)
        self.manager.draw()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView("default", 1.0)
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
