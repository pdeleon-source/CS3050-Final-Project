"""
ManageSound class for handling game soundsn.

This class manages the playing of various sounds such as button presses, moves, captures,
promotions, and castle moves. It implements a singleton pattern to ensure only one instance
of ManageSound exists throughout the program.

Parameters:
- volume (float): The volume level for all sounds, ranging from 0.0 (silent) to 1.0 (full volume).
"""

import arcade

BUTTON_SOUND = "sounds/doink.wav"
MOVE_SOUND = "sounds/make_move.wav"
CAPTURE_SOUND = "sounds/capture.wav"
PROMOTE_SOUND = "sounds/promote.wav"
CASTLE_SOUND = "sounds/castle.wav"

class ManageSound:
    _instance = None  # Private class variable to hold the singleton instance

    def __new__(cls, volume):
        """
        Create a new instance of ManageSound if one doesn't already exist.

        Parameters:
        - volume (float): The initial volume level for all sounds.

        Returns:
        - ManageSound: The ManageSound instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.volume = volume

        return cls._instance

    def get_volume(self):
        """
        Get the current volume level.

        Returns:
        - float: The current volume level, ranging from 0.0 to 1.0.
        """
        return self.volume

    def set_volume(self, volume):
        """
        Set the volume level for all sounds.

        Parameters:
        - volume (float): The new volume level, ranging from 0.0 to 1.0.
        """
        self.volume = volume

    def play_button_sound(self):
        """Play the button press sound."""
        audio = arcade.load_sound(BUTTON_SOUND, False)
        arcade.play_sound(audio, self.volume, -1, False)

    def play_move_sound(self):
        """Play the move sound."""
        move_audio = arcade.load_sound(MOVE_SOUND, False)
        arcade.play_sound(move_audio, self.volume, -1, False)

    def play_capture_sound(self):
        """Play the capture sound."""
        cap_audio = arcade.load_sound(CAPTURE_SOUND, False)
        arcade.play_sound(cap_audio, self.volume, -1, False)

    def play_promote_sound(self):
        """Play the promote sound."""
        promote_audio = arcade.load_sound(PROMOTE_SOUND, False)
        arcade.play_sound(promote_audio, self.volume, -1, False)

    def play_castle_sound(self):
        """Play the castle sound."""
        castle_audio = arcade.load_sound(CASTLE_SOUND, False)
        arcade.play_sound(castle_audio, self.volume, -1, False)
