"""
ManageTheme class for handling theme colors and background in an Arcade-based application.

This class manages the theme colors for the game board, including light and dark square colors
based on the selected theme. It also provides a method to set the background image based on the theme.

Parameters:
- theme (str): The initial theme for the game, such as "default", "midnight", "pink", or "ocean".
"""

import arcade

class ManageTheme:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, theme):
        """
        Create a new instance of ManageTheme if one doesn't already exist.

        Parameters:
        - theme (str): The initial theme for the game.

        Returns:
        - ManageTheme: The ManageTheme instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.theme = theme
            cls._instance.light_square_color, cls._instance.dark_square_color = cls.get_theme(cls._instance, theme)

        return cls._instance

    def get_colors(self):
        """
        Get the light and dark square colors for the current theme.

        Returns:
        - tuple: A tuple containing the light and dark square colors.
        """
        return self.light_square_color, self.dark_square_color

    def set_theme(self, theme):
        """
        Set the theme for the game.

        Parameters:
        - theme (str): The new theme for the game, such as "midnight", "pink", "ocean", or "default".
        """
        if theme == "midnight":
            self.light_square_color = arcade.color.QUEEN_BLUE
            self.dark_square_color = arcade.color.DARK_MIDNIGHT_BLUE
        elif theme == "pink":
            self.light_square_color = arcade.color.CAMEO_PINK
            self.dark_square_color = arcade.color.CHINA_PINK
        elif theme == "ocean":
            self.light_square_color = arcade.color.PALE_ROBIN_EGG_BLUE
            self.dark_square_color = arcade.color.DARK_CYAN
        else:  # Default colors
            self.light_square_color = arcade.color.ALMOND
            self.dark_square_color = arcade.color.SADDLE_BROWN

        self.theme = theme

    def get_theme(self, theme):
        """
        Get the light and dark square colors for a specific theme.

        Parameters:
        - theme (str): The theme to retrieve colors for.

        Returns:
        - tuple: A tuple containing the light and dark square colors for the specified theme.
        """
        if theme == "midnight":
            return arcade.color.QUEEN_BLUE, arcade.color.DARK_MIDNIGHT_BLUE
        elif theme == "pink":
            return arcade.color.CAMEO_PINK, arcade.color.CHINA_PINK
        elif theme == "ocean":
            return arcade.color.PALE_ROBIN_EGG_BLUE, arcade.color.DARK_CYAN
        else:  # Default colors
            return arcade.color.ALMOND, arcade.color.SADDLE_BROWN

    def get_background(self, theme):
        """
        Get the background colors based on the theme for potential use in drawing the background.

        Parameters:
        - theme (str): The theme to retrieve background colors for.

        Returns:
        - tuple: A tuple containing the background color and transparency settings for the specified theme.
        """
        if theme == "midnight":
            return arcade.color.MIDNIGHT_BLUE, (0, 0, 139, 75), (0, 0, 255, 75)
        elif theme == "pink":
            return arcade.color.DUST_STORM, (222, 111, 161, 75), (238, 187, 204, 75)
        elif theme == "ocean":
            return arcade.color.MEDIUM_AQUAMARINE, (0, 0, 255, 75), (173, 216, 230, 75)
        else:  # Default colors
            return arcade.color.BRUNSWICK_GREEN, (139, 69, 19, 75), (234, 222, 203, 75)
