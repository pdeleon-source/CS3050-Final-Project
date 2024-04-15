"""
This program creates a display menu which provides the user with options. The user may
choose to play against a player or a computer or to view tutorials. The user may also
visit a settings menu to change the theme or toggle sound.
"""

import arcade
import board
import time
import tutorial as t
import setting as s
import arcade.gui
from theme_manager import ManageTheme
from sound_manager import ManageSound
import game as g
import arcade.gui.widgets
import arcade.gui.widgets
from arcade.experimental.uistyle import UIFlatButtonStyle


# Find screen measurements
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()

CENTER_WIDTH = SCREEN_WIDTH // 2
CENTER_HEIGHT = SCREEN_HEIGHT // 2

# Set the dimensions of the chessboard
ROWS = 8
COLS = 8
SQUARE_WIDTH = 800 // ROWS
SQUARE_HEIGHT = 800 // COLS

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


class MenuView(arcade.View):
    """
        The main menu. Has options which allow the user to choose a game mode,
        change settings, and quit the game.
    """
    def __init__(self, theme, volume):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        # Define Managers
        global theme_manager, game_manager, sound_manager

        # Open Managers
        theme_manager = ManageTheme("default")
        sound_manager = ManageSound(1)

        # Load game logo
        self.logo = arcade.load_texture("banners/chess_logo.png")
        self.settings_png = arcade.load_texture("assets/settings_cog.png")
        self.tutorial_png = arcade.load_texture("assets/Black_question_mark.png")

        # Create button objects for each option
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
            sound_manager.play_button_sound()
            game_view = g.GameView(theme_manager)
            self.window.show_view(game_view)

        @quit_button.event("on_click")
        def on_click_switch_button(event):
            sound_manager.play_button_sound()
            time.sleep(.15)
            arcade.exit()

        @settings_button.event("on_click")
        def on_click_switch_button(event):
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

        self.manager.add(play_button)
        self.manager.add(tutorial_button)
        self.manager.add(quit_button)
        self.manager.add(settings_button)

        self.game_view = None  # Placeholder for the game view instance


        self.theme_manager = ManageTheme(theme)
        self.volume = volume

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