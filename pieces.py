# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
import arcade
import copy

MOVE_SPEED = 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SQUARE_WIDTH = (SCREEN_WIDTH - 200) // 8
SQUARE_HEIGHT = SCREEN_HEIGHT // 8

"""
TODO: 
dont allow pieces to put their own king in check
force pieces to only have moves that stop their king from being in check
pawn promotion (reaches last row opposing)
check if in check -- this is done in board now, with check_game_over()
check if checkmate -- see above
stalemate (tie, show message) and resign (quit game) -- stalemate is determined in check_game_over()
pinning solution: we really should create a new board state/object to 'test' a move in order to
                  determine if a move will put the king in check due to a pin
"""


class Piece(arcade.AnimatedTimeBasedSprite):
    def __init__(self, allegiance, board, current_pos):
        super().__init__()
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.position = (self.current_col, self.current_row)
        self.board[self.current_row][self.current_col] = self
        self.x = self.current_col * SQUARE_WIDTH + 100
        self.y = self.current_row * SQUARE_HEIGHT
        self.target_x = self.current_col * SQUARE_WIDTH + 100
        self.target_y = self.current_row * SQUARE_HEIGHT
        if self.allegiance == "White":
            self.rank = self.current_row + 1
        else:
            self.rank = abs(8 - self.current_row)

    def draw(self):
        arcade.draw_texture_rectangle((self.x + SQUARE_WIDTH // 2),
                                      self.y + SQUARE_HEIGHT // 2,
                                      SQUARE_WIDTH, SQUARE_HEIGHT,
                                      self.texture)

    def move(self, new_pos) -> bool:
        new_row = new_pos[0]
        new_col = new_pos[1]

        destination = self.board[new_row][new_col]
        if destination is not None and destination.allegiance != self.allegiance:
            print(f"Captured {destination} at position ({new_row}, {new_col})")
        elif destination is not None:
            print(f"Cannot capture {destination}!")
            return False

        # All conditions passed so move Bishop piece
        print(f"Moved {self} to position ({new_row}, {new_col})")

        """
        ---KEEP FOR TESTING PURPOSES---
        

        if isinstance(self, Pawn):
            cap = self.en_passant([new_row, new_col])
            if cap is not None:
                self.board[cap[0]][cap[1]] = None


        self.board[self.current_row][self.current_col] = None
        self.board[new_row][new_col] = self
        """

        if self.allegiance == "White":
            self.rank = new_row + 1
        else:
            self.rank = abs(8 - new_row)

        print(f"{self} Rank = {self.rank}")
        # Update variables
        self.moves += 1
        print(f"{self} Moves = {self.moves}")
        self.current_row = new_row
        self.current_col = new_col

        return True

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
                curr_square = self.board[r][c]
                if curr_square is not None and curr_square.allegiance != self.allegiance:
                    if not isinstance(curr_square, King):
                        # Checks if move would put king in check of another piece
                        movement, captures, attacked = curr_square.available_moves()
                        if (row, col) in attacked :
                                # If not, it gets added to the kings available moves
                                return True
        return False

    def on_click(self, x, y):
        self.target_x = x + (SQUARE_WIDTH // 2) + 100
        self.target_y = y + SQUARE_HEIGHT // 2

        # if self.allegiance == "Black":
        #     print(f"New Pos: {self.target_x} {self.target_y}")
    def update(self):
        # Move the dot towards the target position
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance > MOVE_SPEED:
            scale = MOVE_SPEED / distance
            dx *= scale
            dy *= scale

        self.x += dx
        self.y += dy

    def en_passant(self, position):
        """
        If Pawn and making an en passant move, returns the index of the captured piece
        Otherwise, returns None
        :param position:
        :return row, col:
        """

        if self.allegiance == "White":
            direction = 1
        else:
            direction = -1

        row, col = position[0] - direction, position[1]
        piece = self.board[row][col]
        if isinstance(self, Pawn) and self.rank >= 3:
            if (isinstance(piece, Pawn) and piece.allegiance != self.allegiance
                    and piece.moves == 1 and piece.rank == 4):
                return row, col

        return None

    def promotable(self) -> bool:
        if isinstance(self, Pawn) and self.rank == 8:
            return True
            # change pawn to queen
            # select that particular pawn, change the visual and available moves
        else:
            return False


class Pawn(Piece):
    def __init__(self, allegiance, board, current_pos):
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-pawn.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-pawn.png")

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        moves = []
        caps = []
        attacking = []

        # If the pawn is white, use this set of moves
        if self.allegiance == 'White':
            # NOTE: (1, 0) MUST come before (2, 0) in this list
            pawn_first_moves = [(1, 0), (2, 0)]
            pawn_regular_moves = [(1, 0)]
            pawn_captures = [(1, 1), (1, -1)]
        # If pawn is black, use this set of moves
        else:
            # NOTE: (-1, 0) MUST come before (-2, 0) in this list
            pawn_first_moves = [(-1, 0), (-2, 0)]
            pawn_regular_moves = [(-1, 0)]
            pawn_captures = [(-1, -1), (-1, 1)]

        # If first move
        if self.moves == 0:
            # Attempt first moves
            for pawn_row, pawn_col in pawn_first_moves:
                row, col = self.current_row + pawn_row, self.current_col + pawn_col

                # If row or col off board, try next move
                if 0 > row or row >= 8 or 0 > col or col >= 8:
                    continue

                # If piece in the way, exit loop
                if self.board[row][col] is not None:
                    break
                else:
                    moves.append((row, col))
            # Attempt captures
            for cap_row, cap_col in pawn_captures:
                row, col = self.current_row + cap_row, self.current_col + cap_col
                attacking.append((row, col))
                if 0 > row or row >= 8 or 0 > col or col >= 8:
                    continue

                else:
                # If enemy pawn in square, capture
                    if self.board[row][col] is not None and self.board[row][col].allegiance != self.allegiance:
                        caps.append((row, col))

            return moves, caps, attacking

        # Otherwise it is not first move
        else:
            # Attempt regular moves
            for pawn_row, pawn_col in pawn_regular_moves:
                row, col = self.current_row + pawn_row, self.current_col + pawn_col
                if 0 > row or row >= 8 or 0 > col or col >= 8:
                    continue
                # Append to moves if square is empty
                elif self.board[row][col] is None:
                    moves.append((row, col))
                # If all conditions failed, there are no more possible moves so exit loop
                else:
                    break
            # Attempt captures
            for cap_row, cap_col in pawn_captures:
                row, col = self.current_row + cap_row, self.current_col + cap_col
                attacking.append((row, col))
                if 0 > row or row >= 8 or 0 > col or col >= 8:
                    continue
                else:
                    # If enemy pawn in square, capture
                    if self.board[row][col] is not None and self.board[row][col].allegiance != self.allegiance:
                        caps.append((row, col))

            """En Passant"""
            # Determine direction
            if self.allegiance == "White":
                direction = 1
            else:
                direction = -1

            # Determine possible moves
            move_x = self.current_row + direction
            move_uy = self.current_col + direction
            move_dy = self.current_col - direction

            # Current piece must be at rank 3 or higher
            if self.rank >= 3:
                # Check if enemy pawn to the left
                if self.current_col - 1 > 0:
                    left = self.board[self.current_row][self.current_col - 1]
                    if (isinstance(left, Pawn) and left.allegiance != self.allegiance and
                            0 <= move_x < 8 and 0 <= move_dy < 8):
                        if left.moves == 1 and left.rank == 4:
                            moves.append((move_x, move_dy))

                # Check if enemy pawn to the right
                if self.current_col + 1 < 8:
                    right = self.board[self.current_row][self.current_col + 1]
                    if (isinstance(right, Pawn) and right.allegiance != self.allegiance and
                            0 <= move_x < 8 and 0 <= move_uy < 8):
                        if right.moves == 1 and right.rank == 4:
                            moves.append((move_x, move_uy))

            return moves, caps, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♟'
        return '♙'


class Knight(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
        Extended Constructor for Bishop Piece, adds the texture based on the allegiance of the piece
        :param allegiance: String
        :param board: Board
        :param current_pos: [Int, Int]
        """
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-knight.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-knight.png")

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        movements = []
        captures = []
        attacking = []
        # print(f"{self.current_row} {self.current_col}")
        # Bishop moves diagonally, so we check all four diagonal directions
        for L_row, L_col in [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (-1, -2), (1, -2)]:
            row, col = self.current_row + L_row, self.current_col + L_col
            if 0 <= row < 8 and 0 <= col < 8:
                # print(f"{row} {col}")
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        pass
                        # print(":D")
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        captures.append((row, col))
                        # print(":D")
                else:
                    movements.append((row, col))

                # row += diagonal_row
                # col += diagonal_col
        # print(f"Moves: {movements + captures}")
        return movements, captures, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♞'
        return '♘'

class Rook(Piece):
    def __init__(self, allegiance, board, current_pos):
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-rook.png")
        else:
            self.texture = arcade.load_texture("pieces_png/white-rook.png")

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        moves = []
        caps = []
        attacking = []

        # Try horizontal vals first
        for horiz_row, horiz_col in [(1, 0), (-1, 0)]:
            row, col = self.current_row + horiz_row, self.current_col + horiz_col
            while 0 <= row < 8 and 0 <= col < 8:
                # TODO: Currently, attacking stops updating after it hits a piece
                #       This is an issue if say a rook is covering a row and an
                #       opposing King moves down that row; the square over isn't
                #       being read as attacked
                # TEMP FIX: Add the next square as being attacked in that row/column
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row+1, col))
                        break
                    else:
                        caps.append((row, col))
                        attacking.append((row+1, col))
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
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row, col+1))
                        break
                    else:
                        caps.append((row, col))
                        attacking.append((row, col+1))
                        break
                else:
                    moves.append((row, col))

                row += vert_row
                col += vert_col

        return moves, caps, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♜'
        return '♖'


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

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        """
        Determines the Bishop's valid moves based on its current index
        :return: a list of available moves and a list of potential captures
        """
        movements = []
        captures = []
        attacking = []

        # print(f"{self.current_row} {self.current_col}")
        # Bishop moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                # TODO: Currently, attacking stops updating after it hits a piece
                #       This is an issue if say a rook is covering a row and an
                #       opposing King moves down that row; the square over isn't
                #       being read as attacked
                # TEMP FIX: Add the next square as being attacked in that diagonal
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row+diagonal_row, col+diagonal_col))
                        break
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        captures.append((row, col))
                        attacking.append((row+diagonal_row, col+diagonal_col))
                        break
                else:
                    movements.append((row, col))

                row += diagonal_row
                col += diagonal_col
        # print(f"Moves: {movements + captures}")
        return movements, captures, attacking

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

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        movements = []
        captures = []
        attacking = []

        # Queen moves diagonally, so we check all four diagonal directions
        # Queen also moves horizontally and vertically
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                # TODO: Currently, attacking stops updating after it hits a piece
                #       This is an issue if say a rook is covering a row and an
                #       opposing King moves down that row; the square over isn't
                #       being read as attacked
                # TEMP FIX: Add the next square as being attacked in that row/column
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row+diagonal_row, col+diagonal_col))
                        break
                    else:
                        captures.append((row, col))
                        attacking.append((row+diagonal_row, col+diagonal_col))
                        break
                else:
                    movements.append((row, col))

                row += diagonal_row
                col += diagonal_col

        return movements, captures, attacking

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

    # TODO: We need to implement an 'attacking_squares' return for each piece
    # this way we can track which squares/pieces are under attack and we know
    # if a king can move to a square
    def available_moves(self):
        """
        Determines the King's valid moves based on its current position
        :return: a list of available moves and a list of potential captures
        """
        movements = []
        captures = []
        attacking = []
        # King can move one spot in any direction
        for move_row, move_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            row, col = self.current_row + move_row, self.current_col + move_col
            if 0 <= row < 8 and 0 <= col < 8:
                # If king won't go into check, add to movements
                if not self.under_attack(row, col):
                    attacking.append((row, col))
                    if self.board[row][col] is None:
                        movements.append((row, col))
                    elif self.board[row][col].allegiance != self.allegiance:
                        captures.append((row, col))
                # Otherwise, king is in check - attempt to capture adjacent pieces
                else:
                    if self.board[row][col] is not None and self.board[row][col].allegiance != self.allegiance:
                        captures.append((row, col))

                row += move_row
                col += move_col

        # print(movements)
        return movements, captures, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

    # bish = Bishop("Black", chess_board, 0, 0)
    #bish = Bishop("White", chess_board, [3, 3])
    ###kween = Queen("White", chess_board, [3, 3])
    #king = King("White", chess_board, 2, 2)
    pawn = Pawn("White", chess_board, [0, 1])
    pawn2 = Pawn("Black", chess_board, [7, 2])

    for row in range(7, -1, -1):
        print(chess_board[row])
    print(pawn.available_moves())
    pawn.move([2, 1])
    for row in range(7, -1, -1):
        print(chess_board[row])
    print(pawn.available_moves())
    pawn.move([3, 1])
    for row in range(7, -1, -1):
        print(chess_board[row])
    #print(pawn2.available_moves())
    pawn.move([4, 1])
    for row in range(7, -1, -1):
        print(chess_board[row])
    pawn.move([5, 1])
    for row in range(7, -1, -1):
        print(chess_board[row])

    pawn2.move([5, 2])
    print(pawn2.available_moves())
    for row in range(7, -1, -1):
        print(chess_board[row])
    print(pawn.available_moves())
    print(pawn.en_passant([6, 2]))
    pawn.move([6, 2])

    for row in range(7, -1, -1):
        print(chess_board[row])
