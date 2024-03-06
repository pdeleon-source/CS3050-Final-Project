# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
import board
import arcade


class Piece():
    def __init__(self, allegiance, board, current_pos, texture):
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board[self.current_row][self.current_col] = self

        self.texture = arcade.load_texture(texture)

    def move(self, new_pos) -> bool:
        new_row = new_pos[0]
        new_col = new_pos[1]

        if (new_row, new_col) not in self.available_moves():
            print("INVALID MOVE")
            return False

        destination = self.board[new_row][new_col]
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

"""
class Pawn(Piece):
    def __init__(self, allegiance, board, current_row, current_col):
        points = 1
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_row
        self.current_col = current_col
        self.board = board
        self.board[self.current_col][self.current_row] = self

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
            elif destination[new_row] -  :
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
                return False

    def available_moves(self):
        return []
    def __repr__(self):
        return f"{self.allegiance} Pawn"

class Rook(Piece):
    def __init__(self, allegiance, board, current_row, current_col):
        points = 5
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_row
        self.current_col = current_col
        self.board = board
        self.board[self.current_col][self.current_row] = self

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
"""


class Bishop(Piece):

    def available_moves(self):
        """
        TODO: Check squares in between positions for pieces
        Store in such a way that it shows all indices in between?
        """
        movements = []

        # Bishop moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♝'
        return '♗'


class Queen(Piece):
    def available_moves(self):
        movements = []

        # Queen moves diagonally, so we check all four diagonal directions
        # Queen also moves horizontally and vertically
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        break
                    else:
                        movements.append((row, col))
                        break
                else:
                    movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♛'
        return '♕'


class King(Piece):
    def available_moves(self):
        movements = []
        for move_row, move_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + move_row, self.current_col + move_col
            if 0 <= row < 8 and 0 <= col < 8:
                # If king wont go into check add to movements
                if self.board[row][col] is None or self.board[row][col].allegiance == self.allegiance:
                    movements.append((row, col))

                row += move_row
                col += move_col

        return movements

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

    # bish = Bishop("Black", chess_board, 0, 0)
    #bish = Bishop("White", chess_board, [3, 3])
    king = King("Black", chess_board, [1, 2], "pieces_png/black-king.png")
    queen = Queen("White", chess_board, [2, 2], "pieces_png/white-queen.png")
    #king = King("White", chess_board, 2, 2)

    for row in chess_board:
        print(row)

    print(queen.available_moves())
    print(queen.move([1, 2]))
    move = queen.available_moves()
    print(move)
    for r, c in move:
        print(chess_board[r][c])

    for row in chess_board:
        print(row)
