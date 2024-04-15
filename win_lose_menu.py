"""
WinLoseMenu class for creating a window to display win/lose/draw results and options.
This class provides functionalities to display a win/lose/draw banner and buttons for
replay, main menu, and quitting.
"""

import arcade.gui
import arcade.gui.widgets
import arcade
import time

class WinLoseMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self, theme_manager, winner, game_manager):
        """
        Initialize the WinLoseMenu window.
        Parameters:
        - theme_manager: An instance of ManageTheme class for managing themes.
        - winner (str): The winner of the game ('black', 'white', or 'draw').
        - game_manager: An instance of ManageGame class for managing game states.
        """
        super().__init__(size_hint=(1, 1))

        theme = theme_manager.theme
        self.light_square_color, self.dark_square_color = theme_manager.get_theme(theme)
        self.result = ""
        self.back_clicked = False

        # Setup frame which will act like the window.
        frame = self.add(arcade.gui.UIAnchorLayout(width=500, height=400, size_hint=None))
        frame.with_padding(all=20)

        if winner == "black":
            banner_image = arcade.gui.UISpriteWidget(
                sprite=arcade.Sprite(texture=arcade.load_texture("banners/black_banner.png")),
                width=450,
                height=110)
        elif winner == "white":
            banner_image = arcade.gui.UISpriteWidget(
                sprite=arcade.Sprite(texture=arcade.load_texture("pieces_png/white_banner.png")),
                width=450,
                height=110)
        else:
            banner_image = arcade.gui.UISpriteWidget(
                sprite=arcade.Sprite(texture=arcade.load_texture("banners/draw_banner.png")),
                width=450,
                height=110)

        frame.with_background(texture=arcade.load_texture(
            "assets/grey_panel.png"), start=(7, 7), end=(7, 7))

        # The type of event listener we used earlier for the button will not work here.
        replay_button = arcade.gui.UIFlatButton(text="Replay",
                                                width=350)

        menu_button = arcade.gui.UIFlatButton(text="Main Menu",
                                              width=170)

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=170)

        grid = arcade.gui.UIGridLayout(x=0, y=0, column_count=2, row_count=2, horizontal_spacing=7, vertical_spacing=20)

        grid.add(replay_button, col_num=0, row_num=0, col_span=2)
        grid.add(menu_button, col_num=0, row_num=1)
        grid.add(quit_button, col_num=1, row_num=1)

        widget_layout = arcade.gui.UIBoxLayout(align="center", space_between=0)

        image = arcade.gui.UISpriteWidget(
            sprite=arcade.Sprite(texture=arcade.load_texture("assets/piece_background.png")),
            width=60,
            height=60)

        widget_layout.add(image)
        widget_layout.add(banner_image)

        frame.add(child=widget_layout, anchor_x="center", anchor_y="top")
        frame.add(child=grid, anchor_x="left", anchor_y="top", align_y=-200, align_x=50)

        @replay_button.event("on_click")
        def on_click_switch_button(event):
            """
            Event handler for the Replay button.
            Parameters:
            - event: The event object.
            """
            game_manager.set_game_type("Replay")
            self.parent.remove(self)

        @menu_button.event("on_click")
        def on_click_switch_button(event):
            """
            Event handler for the Main Menu button.
            Parameters:
            - event: The event object.
            """
            game_manager.set_game_type("Main_Menu")
            self.parent.remove(self)

        @quit_button.event("on_click")
        def on_click_switch_button(event):
            """
            Event handler for the Quit button.
            Parameters:
            - event: The event object.
            """
            time.sleep(.15)
            arcade.exit()