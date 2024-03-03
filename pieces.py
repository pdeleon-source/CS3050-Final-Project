# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
import board

class Pawn:
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

    def __repr__(self):
        return f"{self.allegiance} Pawn"

class Rook:
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
            destination = self.board[new_col]
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
            elif destination is not None:
                print("Cannot capture!")
                return False



    def __repr__(self):
        return f"{self.allegiance} Rook"


class Bishop:
    def __init__(self, allegiance, board, current_row, current_col):
        points = 3
        self.moves = 0
        self.allegiance = allegiance
        self.current_row = current_row
        self.current_col = current_col
        self.board = board
        self.board[self.current_col][self.current_row] = self



    def move(self, new_row, new_col) -> bool:
        """
        TODO: Check all squares in between source and destination
        Bishop cannot jump over pieces
        If piece in the way, move invalid
        """
        # Cannot move to same position
        if new_row == self.current_row and new_col == self.current_col:
            print(f"{self} is already in there")
            return False
        # If Bishop is moving diagonally
        elif (new_row + new_col) % 2 == 0:
            destination = self.board[new_row][new_col]
            # Set previous spot to empty
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})!")
            elif destination is not None:
                print("Cannot capture the piece")
                return False

            print(f"Moved {self} to position ({new_row}, {new_col})")

            self.board[self.current_row][self.current_col] = None
            self.board[new_row][new_col] = self

            # Update variables
            self.moves += 1
            self.current_row = new_row
            self.current_col = new_col
            return True
        else:
            print("Invalid move!")
            return False

    def __repr__(self):
        return f"{self.allegiance} Bishop"


class Queen:
    def __init__(self, allegiance, board, current_row, current_col):
        points = 4
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

        # Move diagonally
        elif (new_row + new_col) % 2 == 0 or self.current_row == new_row or self.current_col == new_col:
            destination = self.board[new_row][new_col]
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})")
            elif destination is not None:
                print("Cannot capture that piece!")
                return False

            print(f"Moved {self} to position ({new_row}, {new_col})")
            self.board[self.current_row][self.current_col] = None
            self.board[new_row][new_col] = self

            # Update variables
            self.moves += 1
            self.current_row = new_row
            self.current_col = new_col
            return True
        else:
            print("Invalid move!")
            return False

    def __repr__(self):
        return f"{self.allegiance} Queen"


class King:
    def __init__(self, allegiance, board, current_row, current_col):
        points = 4
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_row
        self.current_col = current_col
        self.board[self.current_col][self.current_row] = self

    def move(self, new_row, new_col):
        destination = self.board[new_row][new_col]
        # Can only move one square
        if new_row == self.current_row and abs(new_col - self.current_col) == 1:
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})")
            elif destination is not None:
                print("Cannot capture that piece!")
                return False

        elif new_col == self.current_col and abs(new_row - self.current_row) == 1:
            if destination is not None and destination.allegiance != self.allegiance:
                print(f"Captured {destination} at position ({new_row}, {new_col})")
            elif destination is not None:
                print("Cannot capture that piece!")
                return False
        else:
            print("Invalid move!")
            return False

        print(f"Moved {self} to position ({new_row}, {new_col})")
        self.board[self.current_row][self.current_col] = None
        self.board[new_row][new_col] = self

        # Update variables
        self.moves += 1
        self.current_row = new_row
        self.current_col = new_col
        return True


    def __repr__(self):
        return f"{self.allegiance} King"


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

   # bish = Bishop("Black", chess_board, 0, 0)
    bish2 = Bishop("White", chess_board, 0, 0)
    queen = Queen("Black", chess_board, 2, 2)
    king = King("White", chess_board, 1, 1)

    for row in chess_board:
        print(row)

    print(king.move(2, 2))

    for row in chess_board:
        print(row)
