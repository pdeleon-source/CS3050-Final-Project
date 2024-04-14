import arcade.gui

import arcade.gui.widgets
import arcade.gui.widgets
from arcade.experimental.uistyle import UIFlatButtonStyle

import arcade

import time

class WinLoseMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self, theme_manager, winner, game_manager):
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
            game_manager.set_game_type("Replay")
            self.parent.remove(self)

        @menu_button.event("on_click")
        def on_click_switch_button(event):
            game_manager.set_game_type("Main_Menu")
            self.parent.remove(self)

        @quit_button.event("on_click")
        def on_click_switch_button(event):
            time.sleep(.15)
            arcade.exit()

    def get_button_color(self, color):
        return UIFlatButtonStyle(
            font_size=12,
            font_name=("calibri", "arial"),
            font_color=arcade.color.BLACK,
            bg=color,
            border=None,
            border_width=2,
        )

    def get_button_styled(self, color):
        return {"normal": self.get_button_color(color),
                "hover": self.get_button_color(color),
                "press": self.get_button_color(color),
                "disabled": self.get_button_color(color)}

    def get_result(self):
        return self.result

    def get_back_clicked(self):
        return self.back_clicked
