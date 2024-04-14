import arcade.gui

import arcade.gui.widgets
import arcade.gui.widgets
from arcade.experimental.uistyle import UIFlatButtonStyle

import time

class SettingsMenu(arcade.gui.UIMouseFilterMixin, arcade.gui.UIAnchorLayout):
    """Acts like a fake view/window."""

    def __init__(self, title: str, toggle_label: str, theme_manager):
        super().__init__(size_hint=(1, 1))

        # Setup frame which will act like the window.
        frame = self.add(arcade.gui.UIAnchorLayout(width=300, height=400, size_hint=None))
        frame.with_padding(all=20)

        # Add a background to the window.
        frame.with_background(texture=arcade.load_texture("pieces_png/grey_panel.png"),
                              end=(25, 25),
                              start=(25, 25))

        # The type of event listener we used earlier for the button will not work here.
        back_button = arcade.gui.UIFlatButton(text="Back", width=250)
        back_button.on_click = self.on_click_back_button

        quit_button = arcade.gui.UIFlatButton(text="Quit", width=250)
        quit_button.on_click = self.on_click_quit_button

        title_label = arcade.gui.UILabel(text=title, align="center", font_size=20, multiline=False,
                                         text_color=arcade.color.BLACK)
        # Adding some extra space around the title.
        title_label_space = arcade.gui.UISpace(height=5, width=250, color=arcade.color.BLACK)

        # Load the on-off textures.
        on_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/checked.png")
        off_texture = arcade.load_texture(":resources:onscreen_controls/shaded_dark/unchecked.png")

        # Create the on-off toggle and a label
        toggle_label = arcade.gui.UILabel(text=toggle_label, text_color=arcade.color.BLACK)
        toggle = arcade.gui.UITextureToggle(
            on_texture=on_texture,
            off_texture=off_texture,
            width=20,
            height=20
        )

        default_button = arcade.gui.UIFlatButton(text="Default",
                                                 width=100,
                                                 height=40,
                                                 style=self.get_button_styled(arcade.color.ALMOND))

        pink_button = arcade.gui.UIFlatButton(text="Pink",
                                              width=100,
                                              height=40,
                                              style=self.get_button_styled(arcade.color.PINK))

        ocean_button = arcade.gui.UIFlatButton(text="Ocean",
                                               width=100,
                                               height=40,
                                               style=self.get_button_styled(arcade.color.OCEAN_BOAT_BLUE))

        midnight_button = arcade.gui.UIFlatButton(text="Midnight",
                                                  width=100,
                                                  height=40,
                                                  style=self.get_button_styled(arcade.color.MIDNIGHT_BLUE))

        grid = arcade.gui.UIGridLayout(column_count=2, row_count=4, horizontal_spacing=13, vertical_spacing=20)

        grid.add(default_button, col_num=0, row_num=0)
        grid.add(pink_button, col_num=1, row_num=0)
        grid.add(ocean_button, col_num=0, row_num=1)
        grid.add(midnight_button, col_num=1, row_num=1)
        grid.add(back_button, col_num=0, row_num=2, col_span=2)
        grid.add(quit_button, col_num=0, row_num=3, col_span=2)

        # Align toggle and label horizontally next to each other
        toggle_group = arcade.gui.UIBoxLayout(vertical=False, space_between=5)
        toggle_group.add(toggle)
        toggle_group.add(toggle_label)

        widget_layout = arcade.gui.UIBoxLayout(align="left", space_between=10)
        widget_layout.add(title_label)
        widget_layout.add(title_label_space)
        widget_layout.add(toggle_group)
        widget_layout.add(grid)
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="top")

        @default_button.event("on_click")
        def on_click_switch_button(event):
            theme_manager.set_theme("default")

        @pink_button.event("on_click")
        def on_click_switch_button(event):
            theme_manager.set_theme("pink")
            print("Theme Change")
            print(theme_manager.theme)

        @ocean_button.event("on_click")
        def on_click_switch_button(event):
            theme_manager.set_theme("ocean")

        @midnight_button.event("on_click")
        def on_click_switch_button(event):
            theme_manager.set_theme("midnight")

    def on_click_back_button(self, event):
        # Removes the widget from the manager.
        # After this the manager will respond to its events like it previously did.
        self.parent.remove(self)

    def on_click_quit_button(self, event):
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
