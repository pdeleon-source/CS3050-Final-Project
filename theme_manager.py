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

# Usage:
theme_manager = ManageTheme("default")
