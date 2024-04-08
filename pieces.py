# for rooks in each turn, one value in the coordinate cannot change
# for bishops, both values must change
from typing import Tuple

import arcade
import copy

MOVE_SPEED = 5
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAPTURE_BOX = 100 // 4

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
                  
                  
TODO: castling!
"""


class Piece(arcade.AnimatedTimeBasedSprite):
    def __init__(self, allegiance, board, current_pos):
        super().__init__()
        self.captured = False
        self.moves = 0
        self.allegiance = allegiance
        self.board = board
        self.current_row = current_pos[0]
        self.current_col = current_pos[1]
        self.temp_current_row = current_pos[0]
        self.temp_current_col = current_pos[1]

        self.position = (self.current_col, self.current_row)
        self.board[self.current_row][self.current_col] = self
        self.x = self.current_col * SQUARE_WIDTH + 100
        self.y = self.current_row * SQUARE_HEIGHT
        self.target_x = self.current_col * SQUARE_WIDTH + 100
        self.target_y = self.current_row * SQUARE_HEIGHT
        if self.allegiance == "White":
            self.rank = self.current_row + 1
            self.value = 1
        else:
            self.rank = abs(8 - self.current_row)
            self.value = -1

    def capture(self):
        self.captured = True

    def draw(self):
        if not self.captured:
            arcade.draw_texture_rectangle((self.x + SQUARE_WIDTH // 2),
                                          self.y + SQUARE_HEIGHT // 2,
                                          SQUARE_WIDTH, SQUARE_HEIGHT,
                                          self.texture)
        else:
            arcade.draw_texture_rectangle(self.x + CAPTURE_BOX // 2,
                                          self.y + CAPTURE_BOX // 2,
                                          CAPTURE_BOX, CAPTURE_BOX,
                                          self.texture)

    def get_value(self):
        return self.value

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
        self.temp_current_col = new_col
        self.temp_current_row = new_row

        return True

    def template_move(self, new_pos, board):
        new_row = new_pos[0]
        new_col = new_pos[1]

        destination = board[new_row][new_col]

        # All conditions passed so move Bishop piece

        if self.allegiance == "White":
            self.rank = new_row + 1
        else:
            self.rank = abs(8 - new_row)

        # Update variables
        self.temp_current_row = new_row
        self.temp_current_col = new_col

        return board

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
                        if (row, col) in attacked:
                            # If not, it gets added to the kings available moves
                            return True
                    else:
                        attacked = []
                        for square_col, square_row in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1),
                                                       (-1, -1)]:
                            final_row = r + square_row
                            final_col = c + square_col
                            if final_row < 0 or final_row > 7 or final_col < 0 or final_col > 7:
                                pass
                            else:
                                attacked.append((final_row, final_col))
                        # print(curr_square.allegiance + " KING ATTACKING SQUARES: ")
                        # print(attacked)
                        if (row, col) in attacked:
                            # If not, it gets added to the kings available moves
                            return True
        return False

    def on_click(self, x, y):
        if not self.captured:
            self.target_x = x + (SQUARE_WIDTH // 2) + 100
            self.target_y = y + SQUARE_HEIGHT // 2
        else:
            self.target_x = x + (CAPTURE_BOX // 2) + 100
            self.target_y = y + CAPTURE_BOX // 2

    # def capture(self, x, y):
    #     self.target_x = x + (CAP_BOX // 2) + 100
    #     self.target_y = y + CAP_BOX // 2

    # if self.allegiance == "Black":
    #     print(f"New Pos: {self.target_x} {self.target_y}")
    def update(self):
        # Move the dot towards the target position
        if not self.captured:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = ((dx ** 2) + (dy ** 2)) ** 0.5
            if distance > MOVE_SPEED:
                scale = MOVE_SPEED / distance
                dx *= scale
                dy *= scale

            self.x += dx
            self.y += dy

    def update_target(self, target_x, target_y):
        self.capture()
        self.x = target_x
        self.y = target_y
        self.target_x = target_x
        self.target_y = target_y

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

    def castle(self, row, col):
        """
            Does the castle. Checks if the king or rook on either side has made any moves, then checks if
            there are any pieces in the first rank between the king and the rook, then returns whether or
            not it is possible
        :return:
        """

        if isinstance(self, King) and self.current_row == row:
            if abs(self.current_col - col) >= 2:
                return True

        return False


        """
        def king_side(self, col):
            if isinstance(self, King) and self.moves == 0:
                # Then check to see if the rook is there
                if isinstance(self, Rook) and self.moves == 0:
                    # if there are no pieces between the king and the rook
                    if self.board[0][col + 1] is None and self.board[0][col + 2] is None:
                        return True

        def queen_side(self, col):
            if isinstance(self, King) and self.moves == 0:
                # Then check to see if the rook is there
                if isinstance(self, Rook) and self.moves == 0:
                    # if there are no pieces between the king and the rook
                    if self.board[0][col - 1] is None and self.board[0][col - 2] is None and self.board[0][col - 3] is None:
                        return True
                    
        """

    def promotable(self) -> bool:
        """
        Returns true if the current piece is a promotable pawn
        :return:
        """
        if isinstance(self, Pawn) and self.rank == 8:
            return True
        else:
            return False


class Pawn(Piece):
    def __init__(self, allegiance, board, current_pos):
        super().__init__(allegiance, board, current_pos)
        if self.allegiance == 'Black':
            self.texture = arcade.load_texture("pieces_png/black-pawn.png")
            self.value = -10
        else:
            self.texture = arcade.load_texture("pieces_png/white-pawn.png")
            self.value = 10
        self.eval = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 5, 5, 5, 5, 5, 5, 5],
            [1, 1, 2, 3, 3, 2, 1, 1],
            [.5, .5, 1, 2.5, 2.5, 1, .5, .5],
            [0, 0, 0, 2, 2, 0, 0, 0],
            [.5, -.5, -1, 0, 0, -1, -.5, .5],
            [.5, 1, 1, -2, -2, 1, 1, .5],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

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
                if self.current_col - direction > 0:
                    left = self.board[self.current_row][self.current_col - direction]
                    if (isinstance(left, Pawn) and left.allegiance != self.allegiance and
                            0 <= move_x < 8 and 0 <= move_dy < 8):
                        if left.moves == 1 and left.rank == 4:
                            moves.append((move_x, move_dy))

                # Check if enemy pawn to the right
                if self.current_col + direction < 8:
                    right = self.board[self.current_row][self.current_col + direction]
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
            self.value = -32
        else:
            self.texture = arcade.load_texture("pieces_png/white-knight.png")
            self.value = 32
        self.eval = [
            [-5, -4, -3, -3, -3, -3, -4, -5],
            [-4, -2, 0, 0, 0, 0, -2, -4],
            [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
            [-3, .5, 1.5, 2, 2, 1.5, .5, -3],
            [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
            [-3, .5, 1, 1.5, 1.5, 1, .1, -3],
            [-4, -2, 0, .5, .5, 0, -2, -4],
            [-5, -4, -3, -3, -3, -3, -4, -5]
        ]

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
            self.value = -50
        else:
            self.texture = arcade.load_texture("pieces_png/white-rook.png")
            self.value = 50
        self.eval = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [.5, 1, 1, 1, 1, 1, 1, .5],
            [-.5, 0, 0, 0, 0, 0, 0, -.5],
            [-.5, 0, 0, 0, 0, 0, 0, -.5],
            [-.5, 0, 0, 0, 0, 0, 0, -.5],
            [-.5, 0, 0, 0, 0, 0, 0, -.5],
            [-.5, 0, 0, 0, 0, 0, 0, -.5],
            [0, 0, 0, .5, .5, 0, 0, 0]
        ]
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
                        attacking.append((row + 1, col))
                        break
                    else:
                        caps.append((row, col))
                        attacking.append((row + 1, col))
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
                        attacking.append((row, col + 1))
                        break
                    else:
                        caps.append((row, col))
                        attacking.append((row, col + 1))
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
            self.value = -33
        else:
            self.texture = arcade.load_texture("pieces_png/white-bishop.png")
            self.value = 33
        self.eval = [
            [-2, -1, -1, -1, -1, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, .5, 1, 1, .5, 0, -1],
            [-1, .5, .5, 1, 1, .5, .5, -1],
            [-1, 0, 1, 1, 1, 1, 0, -1],
            [-1, 1, 1, 1, 1, 1, 1, -1],
            [-1, .5, 0, 0, 0, 0, .5, -1],
            [-2, -1, -1, -1, -1, -1, -1, -2]
        ]

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
                        attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        captures.append((row, col))
                        attacking.append((row + diagonal_row, col + diagonal_col))
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
            self.value = -90
        else:
            self.texture = arcade.load_texture("pieces_png/white-queen.png")
            self.value = 90
        self.eval = [
            [-2, -1, -1, -.5, -.5, -1, -1, -2],
            [-1, 0, 0, 0, 0, 0, 0, -1],
            [-1, 0, .5, .5, .5, .5, 0, -1],
            [-.5, 0, .5, .5, .5, .5, 0, -.5],
            [0, 0, .5, .5, .5, .5, 0, -.5],
            [-1, .5, .5, .5, .5, .5, 0, -1],
            [-1, 0, .5, 0, 0, 0, 0, -1],
            [-2, -1, -1, -.5, -.5, -1, -1, -2]
        ]

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
                        attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                    else:
                        captures.append((row, col))
                        attacking.append((row + diagonal_row, col + diagonal_col))
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
            self.value = -900
        else:
            self.texture = arcade.load_texture("pieces_png/white-king.png")
            self.value = 900
        self.eval = [
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-3, -4, -4, -5, -5, -4, -4, -3],
            [-2, -3, -3, -4, -4, -3, -3, -2],
            [-1, -2, -2, -2, -2, -2, -2, -1],
            [2, 2, 0, 0, 0, 0, 2, 2],
            [2, 3, 1, 0, 0, 1, 3, 2]
        ]

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
                attacking.append((row, col))
                # If king won't go into check, add to movements
                if not self.under_attack(row, col):
                    if self.board[row][col] is None:
                        movements.append((row, col))
                    elif self.board[row][col].allegiance != self.allegiance:
                        captures.append((row, col))
                # Otherwise, king is in check - attempt to capture adjacent pieces
                # else:
                #     if self.board[row][col] is not None and self.board[row][col].allegiance != self.allegiance:
                #         captures.append((row, col))

                row += move_row
                col += move_col
        left = self.board[self.current_row][self.current_col - 4]
        right = self.board[self.current_row][self.current_col + 3]

        row = self.current_row
        left_none = self.current_col - 2
        left_rook = self.current_col - 4
        right_none = self.current_col + 2
        right_rook = self.current_col + 3

        # If there is a rook to the left
        if isinstance(left, Rook) and left.moves == 0 and left.allegiance == self.allegiance:
            if (self.board[self.current_row][self.current_col - 1] is None and
                    self.board[self.current_row][self.current_col - 2] is None
                    and self.board[self.current_row][self.current_col - 3] is None):

                attacking.append((row, left_none))
                attacking.append((row, left_rook))

                if not self.under_attack(row, left_none):
                    movements.append((row, left_none))
                if not self.under_attack(row, left_rook):
                    movements.append((row, left_rook))

        # If there is a rook to the right
        if isinstance(right, Rook) and right.moves == 0 and right.allegiance == self.allegiance:
            if (self.board[self.current_row][self.current_col + 1] is None and
                    self.board[self.current_row][self.current_col + 2] is None):
                attacking.append((self.current_row, right_none))
                attacking.append((self.current_row, right_rook))

                if not self.under_attack(row, right_none):
                    movements.append((self.current_row, right_none))
                if not self.under_attack(row, right_rook):
                    movements.append((self.current_row, right_rook))

        return movements, captures, attacking

    def castle(self):
        # check to see it is a king is in its original position
        if isinstance(self, King) and self.moves == 0:
            # Then check to see if the rook is there
            if isinstance(self, Rook) and self.rank >= 3:
                pass
            # Then check to see if there ae no pieces between the king and rook

            # Then do the switch

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'


if __name__ == "__main__":
    chess_board = [[None for _ in range(8)] for _ in range(8)]

    # bish = Bishop("Black", chess_board, 0, 0)
    # bish = Bishop("White", chess_board, [3, 3])
    ###kween = Queen("White", chess_board, [3, 3])
    # king = King("White", chess_board, 2, 2)
    white_king = King("White", chess_board, [0, 4])
    black_king = King("Black", chess_board, [7, 4])
    white_rook_left = Rook("White", chess_board, [0, 0])
    white_rook_right = Rook("White", chess_board, [0, 7])
    black_rook_left = Rook("Black", chess_board, [7, 0])
    black_rook_right = Rook("Black", chess_board, [7, 7])

    for row in range(7, -1, -1):
        print(chess_board[row])

    print(white_king.available_moves())
    print(black_king.available_moves())

