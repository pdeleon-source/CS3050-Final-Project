import arcade

class ManageTheme:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, theme):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.theme = theme
            cls._instance.light_square_color, cls._instance.dark_square_color = cls.get_theme(cls._instance, theme)

        return cls._instance

    def get_colors(self):
        return self.light_square_color, self.dark_square_color

    def set_theme(self, theme):
        if theme == "midnight":
            self.light_square_color = arcade.color.BLUE
            self.dark_square_color = arcade.color.DARK_BLUE
        elif theme == "pink":
            self.light_square_color = arcade.color.CAMEO_PINK
            self.dark_square_color = arcade.color.CHINA_PINK
        elif theme == "ocean":
            self.light_square_color = arcade.color.LIGHT_BLUE
            self.dark_square_color = arcade.color.BLUE
        else:  # Default colors
            self.light_square_color = arcade.color.ALMOND
            self.dark_square_color = arcade.color.SADDLE_BROWN

        self.theme = theme

    def get_theme(self, theme):
        if theme == "midnight":
            return arcade.color.BLUE, arcade.color.DARK_BLUE
        elif theme == "pink":
            return arcade.color.CAMEO_PINK, arcade.color.CHINA_PINK
        elif theme == "ocean":
            return arcade.color.LIGHT_BLUE, arcade.color.BLUE
        else:  # Default colors
            return arcade.color.ALMOND, arcade.color.SADDLE_BROWN

    """
    if self.theme == "midnight":
        background = arcade.load_texture("pieces_png/midnight1.jpg")
        background.draw_sized(center_x=SCREEN_WIDTH/2, center_y=SCREEN_HEIGHT/2,
                              width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

    elif self.theme == "ocean":
        background = arcade.load_texture("pieces_png/ocean.jpg")
        background.draw_sized(center_x=SCREEN_WIDTH / 2, center_y=SCREEN_HEIGHT / 2,
                              width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    """

    def get_background(self, theme):
        # TODO: Pass in theme manager object instead?
        """Set colors based on theme"""
        if theme == "midnight":
            return arcade.color.MIDNIGHT_BLUE, (0, 0, 139, 75), (0, 0, 255, 75)
        elif theme == "pink":
            return arcade.color.DUST_STORM, (222, 111, 161, 75), (238, 187, 204, 75)
        elif theme == "ocean":
            return arcade.color.OCEAN_BOAT_BLUE, (0, 0, 255, 75), (173, 216, 230, 75)
        else:  # Default colors
            return arcade.color.BRUNSWICK_GREEN, (139, 69, 19, 75), (234, 222, 203, 75)

# Usage:
theme_manager = ManageTheme("default")
