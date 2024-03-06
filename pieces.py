# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
import board
import arcade


class Piece:
    def __init__(self, allegiance, board, current_pos):
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.board[self.current_row][self.current_col] = self

    def move(self, new_pos) -> bool:
        new_row = new_pos[0]
        new_col = new_pos[1]

        possible_moves = self.available_moves()[0] + self.available_moves()[1]

        if (new_row, new_col) not in possible_moves:
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

# class Pawn(Piece):
#     def __init__(self, allegiance, board, current_pos):
#         super().__init__(allegiance, board, current_pos)
#         if self.allegiance == 'Black':
#             self.texture = arcade.load_texture("pieces_png/black-pawn.png")
#         else:
#             self.texture = arcade.load_texture("pieces_png/white-pawn.png")
#
#     def move(self, new_row, new_col):
#         if new_row == self.current_row and new_col == self.current_col:
#             print(f"{self} is already in that position!")
#             return False
#         # account for two block move on the first turn
#         elif self.moves == 0 and new_row - self.current_row == 2 and new_col == self.current_col:
#             destination = self.board[new_row][new_col]
#         # now account for a normal move
#         elif self.moves >= 1 and new_row - self.current_row == 1 and new_col == self.current_col:
#             destination = self.board[new_row][new_col]
#         # now account for captures-a diagonal movement
#         elif (new_row + new_col) % 2 == 0:
#             destination = self.board[new_row][new_col]
#             if destination is not None and destination.allegiance != self.allegiance:
#                 print(f"Captured {destination} at position ({new_row}, {new_col})!")
#             # en passant-hard as hell, how do I get the space under the destination block?
#             elif destination[new_row]:
#                 print(f"Captured {destination} at position ({new_row}, {new_col})!")
#                 return False
#
#     def available_moves(self):
#         moves = []
#         caps = []
#
#
#     def __repr__(self):
#         return f"{self.allegiance} Pawn"

class Rook(Piece):
    def __init__(self, allegiance, board, current_pos):
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-rook.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-rook.png")

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

    def available_moves(self):
        moves = []
        caps = []

        # Try horizontal vals first
        for horiz_row, horiz_col in [(1, 0), (-1, 0)]:
            row, col = self.current_row + horiz_row, self.current_col + horiz_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        break
                    else:
                        caps.append((row, col))
                        break
                else:
                    moves.append((row, col))

                row += horiz_row
                col += horiz_col
        # an or statement here?
        # vertical vals
        for vert_row, vert_col in [(0, 1), (0, -1)]:
            row, col = self.current_row + vert_row, self.current_col + vert_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        break
                    else:
                        caps.append((row, col))
                        break
                else:
                    moves.append((row, col))

                row += vert_row
                col += vert_col

        return moves, caps

class Bishop(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
        Extended Constructor for Bishop Piece, adds the texture based on the allegiance of the piece
        :param allegiance: String
        :param board: Board
        :param current_pos: [Int, Int]
        """
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-bishop.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-bishop.png")

    def available_moves(self):
        movements = []
        captures = []

        # Bishop moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        break
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        captures.append((row, col))
                        break
                else:
                    movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        return movements, captures

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♝'
        return '♗'


class Queen(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
        Extended Constructor for Queen Piece, adds the texture based on the allegiance of the piece
        :param allegiance: String
        :param board: Board
        :param current_pos: [Int, Int]
        """
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-queen.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-queen.png")

    def available_moves(self):
        movements = []
        captures = []

        # Queen moves diagonally, so we check all four diagonal directions
        # Queen also moves horizontally and vertically
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        break
                    else:
                        captures.append((row, col))
                        break
                else:
                    movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        return movements, captures

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♛'
        return '♕'


class King(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
        Extended Constructor for King Piece, adds the texture based on the allegiance of the piece
        :param allegiance: String
        :param board: Board
        :param current_pos: [Int, Int]
        """
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-king.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-king.png")

    def available_moves(self):
        """
        TODO: allow capture if King in check
        """
        movements = []
        captures = []
        for move_row, move_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + move_row, self.current_col + move_col
            if 0 <= row < 8 and 0 <= col < 8:
                # If king won't go into check add to movements
                if not self.under_attack(row, col):
                    if self.board[row][col] is None:
                        movements.append((row, col))
                    elif self.board[row][col].allegiance != self.allegiance:
                        captures.append((row, col))
                # King is under attack - try to capture
                else:
                    if self.board[row][col] is not None and self.board[row][col].allegiance != self.allegiance:
                        captures.append((row, col))

                row += move_row
                col += move_col

        return movements, captures

    def under_attack(self, row, col) -> bool:
        """
        Checks if the given move will put the king under attack
        :param row:
        :param col:
        :return:
        """

        # Loops through the board
        for r in range(8):
            for c in range(8):
                # Finds pieces of a different allegiance, who are not a king
                if self.board[r][c] is not None and self.board[r][c].allegiance != self.allegiance:
                    if not isinstance(self.board[r][c], King):
                        # Checks if move would put king in check of another piece
                        movement, captures = self.board[r][c].available_moves()
                        if (row, col) in captures or (row, col) in movement:
                            # If not, it gets added to the kings available moves
                            return True
        return False

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

    # bish = Bishop("Black", chess_board, 0, 0)
    #bish = Bishop("White", chess_board, [3, 3])
    king = King("Black", chess_board, [0, 1])
    queen = Queen("White", chess_board, [2, 2])
    kween = Queen("White", chess_board, [3, 3])
    #king = King("White", chess_board, 2, 2)

    for row in chess_board:
        print(row)
    print(king.available_moves())
    print(queen.available_moves())
    queen.move([1, 2], chess_board)
    print("QUEEN MOVES")
    for row in chess_board:
        print(row)
    #bish.move([2, 2], chess_board)

    print("KING MOVES")
    king.move([1, 2], chess_board)

    for row in chess_board:
        print(row)

    kween.move([2, 2], chess_board)
    print("KWEEN MOVES")
    for row in chess_board:
        print(row)
    print("King's moves.....")
    print(king.available_moves())



    print("KING CAPTURES")
    king.move([2, 2], chess_board)
    for row in chess_board:
        print(row)
