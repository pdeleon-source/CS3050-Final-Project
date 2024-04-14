class ManageGame:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, game_type):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.game_type = game_type

        return cls._instance

    def get_game_type(self):
        return self.game_type

    def set_game_type(self, new_type):
        self.game_type = new_type
