import board
import arcade

# Set the dimensions of the chessboard
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

if __name__ == "__main__":
    window = board.Board()
    #arcade.run()
    window.show_view(board_view)
