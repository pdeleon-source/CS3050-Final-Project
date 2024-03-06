# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
import board
import arcade

class Piece():
    def something(self):
        print("something")

class Pawn(Piece):
    def __init__(self, allegiance, board, current_pos):
        points = 1
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board = board
        if allegiance == 'Black':
            self.texture = arcade.load_texture('pieces_png/black-pawn.png')
        else:
            self.texture = arcade.load_texture('pieces_png/white-pawn.png')

    def move(self, new_row, new_col):
        if new_row == self.current_row and new_col == self.current_col:
            print(f"{self} is already in that position!")
            return False
        # account for two block move on the first turn
        elif self.moves == 0 and new_row - self.current_row == 2 and new_col == self.current_col:
            destination = self.board[new_row][new_col]
        # now account for a normal move
        elif self.moves >= 1 and new_row - self.current_row == 1 and new_col == self.current_col:
            destination = self.board[new_row][new_col]
        # now account for captures-a diagonal movement
        elif (new_row + new_col) % 2 == 0:
            destination = self.board[new_row][new_col]
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
            # en passant-hard as hell, how do I get the space under the destination block?
            elif destination[new_row]:
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
                return False

    def available_moves(self):
        return []
    def __repr__(self):
        return f"{self.allegiance} Pawn"

class Rook(Piece):
    def __init__(self, allegiance, board, current_pos):
        points = 5
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board = board
        if allegiance == 'Black':
            self.texture = arcade.load_texture('pieces_png/black-rook.png')
        else:
            self.texture = arcade.load_texture('pieces_png/white-rook.png')

    def move(self, new_row, new_col):
        # Cannot move to same position
        if new_row == self.current_row and new_col == self.current_col:
            print(f"{self} is already there")
            return False
        # horizontal movement
        elif new_row != self.current_row and new_col == self.current_col:
            destination = self.board[new_row]
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
            elif destination is not None:
                print("Cannot capture")
                return False
        # vertical movement
        elif new_row == self.current_row and new_col != self.current_col:
            destination = self.board[new_row][new_col]
class Bishop(Piece):
    def __init__(self, allegiance, board, current_pos):
        points = 3
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board = board
        #self.board[self.current_col][self.current_row] = self
        if allegiance == 'Black':
            self.texture = arcade.load_texture('pieces_png/black-bishop.png')
        else:
            self.texture = arcade.load_texture('pieces_png/white-bishop.png')

    def move(self, new_row, new_col, board) -> bool:
        """
        TODO: Check all squares in between source and destination
        Bishop cannot jump over pieces
        If piece in the way, move invalid
        """
        # self.board = board

        if (new_row, new_col) not in self.available_moves():
            print("INVALID MOVE")
            return False

        destination = self.board[new_row][new_col]
        print(destination)
        if destination is not None and destination.allegiance != self.allegiance:
            print(f"Captured {destination} at position ({new_row}, {new_col})")
        elif destination is not None:
            print(f"Cannot capture {destination}!")
            return False

        # All conditions passed so move Bishop piece
        print(f"Moved {self} to position ({new_row}, {new_col})")

        self.board[self.current_row][self.current_col] = None
        self.board[new_row][new_col] = self

        # Update variables
        self.moves += 1
        self.current_row = new_row
        self.current_col = new_col
        return True

    def available_moves(self):
        movements = []

        # Bishop moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is None:
                    movements.append((row, col))
                    row += diagonal_row
                    col += diagonal_col
                else:
                    movements.append((row, col))
                    break

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♝'
        return '♗'


class Queen(Piece):
    def __init__(self, allegiance, board, current_pos):
        points = 4
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board = board
        # self.board[self.current_col][self.current_row] = self
        if allegiance == 'Black':
            self.texture = arcade.load_texture('pieces_png/black-queen.png')
        else:
            self.texture = arcade.load_texture('pieces_png/white-queen.png')

    def move(self, new_row, new_col) -> bool:
        if (new_row, new_col) not in self.available_moves():
            print("INVALID MOVE!")
            return False
        destination = self.board[new_row][new_col]
        if destination is not None and destination.allegiance != self.allegiance:
            print(f"Captured {destination} at position ({new_row}, {new_col})")
        elif destination is not None:
            print("Cannot capture that piece!")

        print(f"Moved {self} to position ({new_row}, {new_col})")

        self.board[self.current_row][self.current_col] = None
        self.board[new_row][new_col] = self

        # Update variables
        self.moves += 1
        self.current_row = new_row
        self.current_col = new_col
        return True

    def available_moves(self):
        movements = []

        # Queen moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        # Queen may also move vertically and horizontally
        # TODO: Includes current position
        for i in range(0, 8):
            movements.append((self.current_row, i))
            movements.append((i, self.current_col))

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♛'
        return '♕'

        # return f"{self.allegiance} Queen"


class King(Piece):
    def __init__(self, allegiance, board, current_pos):
        points = 4
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        #self.board[self.current_row][self.current_col] = self
        if allegiance == 'Black':
            self.texture = arcade.load_texture('pieces_png/black-king.png')
        else:
            self.texture = arcade.load_texture('pieces_png/white-king.png')

    def move(self, new_row, new_col) -> bool:
        if (new_row, new_col) not in self.available_moves():
            print("INVALID MOVE!")
            return False

        destination = self.board[new_row][new_col]
        if destination is not None and destination.allegiance != self.allegiance:
            print(f"Captured {destination} at position ({new_row}, {new_col})")
        elif destination is not None:
            print("Cannot capture that piece!")

        print(f"Moved {self} to position ({new_row}, {new_col})")
        self.board[self.current_row][self.current_col] = None
        self.board[new_row][new_col] = self

        # Update variables
        self.moves += 1
        self.current_row = new_row
        self.current_col = new_col
        return True

    def available_moves(self):
        movements = []

        movements.append((self.current_row - 1, self.current_col))
        movements.append((self.current_row - 1, self.current_col + 1))
        movements.append((self.current_row - 1, self.current_col - 1))

        movements.append((self.current_row, self.current_col))
        movements.append((self.current_row, self.current_col + 1))
        movements.append((self.current_row, self.current_col - 1))

        movements.append((self.current_row + 1, self.current_col))
        movements.append((self.current_row + 1, self.current_col + 1))
        movements.append((self.current_row + 1, self.current_col - 1))

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'

        # return f"{self.allegiance} King"


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

    # bish = Bishop("Black", chess_board, 0, 0)
    #bish = Bishop("White", chess_board, [3, 3])
    king = King("Black", chess_board, [1, 2])
    #king = King("White", chess_board, 2, 2)

    for row in chess_board:
        print(row)

    print(king.available_moves())

    for row in chess_board:
        print(row)
