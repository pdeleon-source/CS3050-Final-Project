class MenuView(arcade.View):
    def __init__(self, theme):
        super().__init__()
        # Other initialization code...

        self.manager = arcade.gui.UIManager()
        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        # Create the submenu
        self.submenu = t.SubMenu(
            "Tutorial Menu",  # Change to your desired submenu title
            "This is a tutorial submenu.",  # Change to your desired submenu description
            "OK"  # Change to your desired submenu button label
        )
        self.manager.add(self.submenu)

        # Other initialization code...

    def on_mouse_press(self, x, y, button, modifiers):
        super().on_mouse_press(x, y, button, modifiers)
        self.play_button.on_mouse_press(x, y, button, modifiers)
        self.tutorial_button.on_mouse_press(x, y, button, modifiers)
        self.settings_button.on_mouse_press(x, y, button, modifiers)
        self.quit_button.on_mouse_press(x, y, button, modifiers)

        if self.tutorial_button.is_clicked:
            self.manager.draw()  # Display the submenu

    def update(self, delta_time):
        super().update(delta_time)
        if self.tutorial_button.is_clicked:
            if self.submenu.button.is_clicked:
                self.manager.pop_view()  # Close the submenu if the button inside it is clicked
