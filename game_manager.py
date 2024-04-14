"""
ManageGame class for handling the type of game function the user wants to perform after ending a
game. This tells us if they want to replay the game or go back to the main meny.

Parameters:
- game_type (str): The initial game type, "_"
"""


class ManageGame:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, game_type):
        """
        Create a new instance of ManageGame if one doesn't already exist.

        Parameters:
        - game_type (str): The initial game type.

        Returns:
        - ManageGame: The ManageGame instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.game_type = game_type

        return cls._instance

    def get_game_type(self):
        """
        Get the current game type.

        Returns:
        - str: The current game type.
        """
        return self.game_type

    def set_game_type(self, new_type):
        """
        Set the game type to a new value.

        Parameters:
        - new_type (str): The new game type, such as "Replay" or "Main_Menu".
        """
        self.game_type = new_type
