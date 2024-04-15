"""
    This program implements the functionality for all the pieces in the game. It has a Piece superclass
    and subclasses to represent the Pawn, Rook, Bishop, Knight, Queen, and King.
"""

import arcade

# Define constants
MOVE_SPEED = 5
SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
CAPTURE_BOX = 100 // 4

BOARD_WIDTH = 800
BOARD_HEIGHT = 600

SQUARE_WIDTH = (BOARD_WIDTH - 200) // 8
SQUARE_HEIGHT = BOARD_HEIGHT // 8


class Piece(arcade.AnimatedTimeBasedSprite):
    """
        Piece acts as a superclass which holds functions used by all the Piece subclasses
        to move pieces, print to board, etc.
    """
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

        self.is_moving = False

        self.position = (self.current_col, self.current_row)
        self.board[self.current_row][self.current_col] = self

        self.x = self.current_col * SQUARE_WIDTH + (SCREEN_WIDTH / 3.25)
        self.y = self.current_row * SQUARE_HEIGHT + (SCREEN_HEIGHT // 6)
        self.target_x = self.current_col * SQUARE_WIDTH + (SCREEN_WIDTH / 3.25)
        self.target_y = self.current_row * SQUARE_HEIGHT + (SCREEN_HEIGHT // 6)
        if self.allegiance == "White":
            self.rank = self.current_row + 1
            self.value = 1
        else:
            self.rank = abs(8 - self.current_row)
            self.value = -1

    def capture(self):
        self.captured = True

    def draw(self):
        arcade.draw_texture_rectangle((self.x + SQUARE_WIDTH // 2),
                                      self.y + SQUARE_HEIGHT // 2,
                                      SQUARE_WIDTH, SQUARE_HEIGHT,
                                      self.texture)

    def get_value(self):
        return self.value

    def move(self, new_pos):
        """
            The move function takes in the row and the column that the piece will move to
            and updates its current position on the board accordingly.
            :param new_pos: # A list containing the row and column, respectfully
        """
        new_row = new_pos[0]
        new_col = new_pos[1]

        # Get rank based on allegiance
        if self.allegiance == "White":
            self.rank = new_row + 1
        else:
            self.rank = abs(8 - new_row)

        # Update variables based on move
        self.moves += 1
        self.current_row = new_row
        self.current_col = new_col
        self.temp_current_col = new_col
        self.temp_current_row = new_row

    def test_player_move(self, new_pos, board) -> bool:
        """
            The test_player_move function checks if a given move will put or keep
            its king in check. Does not actually make a move, but tests possible moves.
            :param new_pos:
            :param board:
            :return bool:
        """
        og_row = self.current_row
        og_col = self.current_col
        new_row = new_pos[0]
        new_col = new_pos[1]

        destination = board[new_row][new_col]

        # If capture
        if destination is not None and destination.allegiance != self.allegiance:
            pass
        # If its own piece
        elif destination is not None and destination.allegiance == self.allegiance:
            return False

        # Record and attempt move
        self.temp_current_row = new_row
        self.temp_current_col = new_col

        board[new_row][new_col] = self
        board[og_row][og_col] = None

        # Find the king on the board
        for row in range(8):
            for col in range(8):
                square = board[row][col]
                if isinstance(square, King):
                    if square.allegiance == self.allegiance:
                        # If the king is still in check, return false
                        king_in_check = square.under_attack(row, col)
                        if not king_in_check:
                            board[og_row][og_col] = self
                            board[new_row][new_col] = destination
                            return True
                        else:
                            board[og_row][og_col] = self
                            board[new_row][new_col] = destination
                            return False

    def template_move(self, new_pos, board):
        """
            The template_move function makes a temporary move for testing purposes.
            Allows us to check if a given move is valid by returning the resulting board
            after making a temporary move.
            :param new_pos:
            :param board:
            :return board:
        """

        new_row = new_pos[0]
        new_col = new_pos[1]

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
        Checks if the given move will put the king under attack / in check
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
                        movement, captures, attacked = curr_square.available_moves(True)
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
                        if (row, col) in attacked:
                            return True
        return False

    def on_click(self, x, y):
        if not self.captured:
            self.target_x = x
            self.target_y = y
            self.is_moving = True
        else:
            self.target_x = x + (CAPTURE_BOX // 2) + 100
            self.target_y = y + CAPTURE_BOX // 2

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

        if self.target_x == self.x and self.target_y == self.y:
            self.is_moving = False

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
        if not isinstance(self, Pawn):
            return None

        # Change direction of move based on allegiance
        if self.allegiance == "White":
            direction = 1
        else:
            direction = -1

        # Check if pawn is currently making an en passant move
        row, col = position[0] - direction, position[1]
        piece = self.board[row][col]
        if isinstance(self, Pawn) and self.rank >= 3:
            if (isinstance(piece, Pawn) and piece.allegiance != self.allegiance
                    and piece.moves == 1 and piece.rank == 4):
                return row, col

        return None

    def promotable(self) -> bool:
        """
        Returns true if the current piece is a promotable pawn
        :return:
        """
        if isinstance(self, Pawn) and self.rank == 8 and self.moves >= 5:
            return True
        else:
            return False

    def check_castle(self, row, col):
        """
            Checks if the given move is a castle move. Returns the row, the column of the nearest
            rook, and the column the rook will move to. Returns None if not castle move.
            :param row:
            :param col:
            :return row, rook_col, new_rook_col:
        """
        # Return None if castle not possible
        if not isinstance(self, King) or self.moves != 0 or abs(self.current_col - col) < 2:
            return None

        destination = self.board[row][col]
        # If player chooses rook spot
        if isinstance(destination, Rook):
            # Return rook future position
            # If left rook
            if col == 0:
                return row, col, col + 1
            # If right rook
            else:
                return row, col, col - 1
        # If player chooses empty spot
        elif destination is None:
            if col == 6:
                return row, 7, col - 1  # Rook at position 7
            elif col == 2 or col == 1:
                return row, 0, col + 1  # Rook at position 0

        return None


class Pawn(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
            Extended Constructor for Pawn Piece, adds the texture based on the allegiance of the piece
            :param allegiance: String
            :param board: Board
            :param current_pos: [Int, Int]
        """
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

    def available_moves(self, testing_move):
        """
            Records valid moves available for the pawn. Pawns can move one or two squares
            forward on their first move and one square forward otherwise. Pawns capture enemy
            pieces diagonally. Pawns may also make en passant moves.
            :param testing_move:
            :return movements, captures, attacking:
        """
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

        # If pawn's first move
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
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
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
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
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
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
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
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                caps.append((row, col))

            """ En Passant """
            # Determine direction based on allegiance
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
                if 0 < self.current_col - direction < 8:
                    left = self.board[self.current_row][self.current_col - direction]

                    if (isinstance(left, Pawn) and left.allegiance != self.allegiance and
                            0 <= move_x < 8 and 0 <= move_dy < 8):
                        if left.moves == 1 and left.rank == 4:
                            if not testing_move:
                                if self.test_player_move((row, col), self.board):
                                    moves.append((move_x, move_dy))

                # Check if enemy pawn to the right
                if 0 < self.current_col + direction < 8:
                    right = self.board[self.current_row][self.current_col + direction]

                    if (isinstance(right, Pawn) and right.allegiance != self.allegiance and
                            0 <= move_x < 8 and 0 <= move_uy < 8):
                        if right.moves == 1 and right.rank == 4:
                            if not testing_move:
                                if self.test_player_move((row, col), self.board):
                                    moves.append((move_x, move_uy))

            return moves, caps, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♟'
        return '♙'


class Knight(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
        Extended Constructor for Knight Piece, adds the texture based on the allegiance of the piece
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

    def available_moves(self, testing_move):
        """
            Records valid moves available for the knight. The knight may move two squares horizontally
            and one square vertically, or one square horizontally and two squares vertically.
            :param testing_move:
        """
        movements = []
        captures = []
        attacking = []

        # Knight moves in L shapes
        for L_row, L_col in [(2, -1), (2, 1), (-2, -1), (-2, 1), (1, 2), (-1, 2), (-1, -2), (1, -2)]:
            row, col = self.current_row + L_row, self.current_col + L_col
            if 0 <= row < 8 and 0 <= col < 8:
                attacking.append((row, col))
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        pass
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                captures.append((row, col))
                else:
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
                            movements.append((row, col))

        return movements, captures, attacking

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♞'
        return '♘'


class Rook(Piece):
    def __init__(self, allegiance, board, current_pos):
        """
            Extended Constructor for Rook Piece, adds the texture based on the allegiance of the piece
            :param allegiance: String
            :param board: Board
            :param current_pos: [Int, Int]
        """
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

    def available_moves(self, testing_move):
        """
            Records valid moves available for the rook. The rook can move vertically and horizontally
            as many squares as it likes as long as there is not a piece in the way.
            :param testing_move:
            :return movements, captures, attacking:
        """
        moves = []
        caps = []
        attacking = []

        # Try horizontal values first
        for horiz_row, horiz_col in [(1, 0), (-1, 0)]:
            row, col = self.current_row + horiz_row, self.current_col + horiz_col
            while 0 <= row < 8 and 0 <= col < 8:
                attacking.append((row, col))
                # There is a piece in the way
                if self.board[row][col] is not None:
                    # Capture if enemy piece and exit loop
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row + horiz_row, col + horiz_col))
                        break
                    else:
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                caps.append((row, col))
                            if isinstance(self.board[row][col], King):
                                attacking.append((row + horiz_row, col + horiz_col))
                        break
                # Add empty squares to moves
                else:
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
                            attacking.append((row + horiz_row, col + horiz_col))
                            moves.append((row, col))

                row += horiz_row
                col += horiz_col

        # Vertical values
        for vert_row, vert_col in [(0, 1), (0, -1)]:
            row, col = self.current_row + vert_row, self.current_col + vert_col
            while 0 <= row < 8 and 0 <= col < 8:
                attacking.append((row, col))
                # There is a piece in the way
                if self.board[row][col] is not None:
                    # Capture if enemy piece and exit loop
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row + vert_row, col + vert_col))
                        break
                    else:
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                caps.append((row, col))
                        if isinstance(self.board[row][col], King):
                            attacking.append((row + vert_row, col + vert_col))
                        break
                # Add empty squares to moves
                else:
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
                            attacking.append((row + vert_row, col + vert_col))
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

    def available_moves(self, testing_move):
        """
            Records valid moves available for the bishop. Bishops may move diagonally in any
            direction as long as there is not a piece in the way.
            :param testing_move:
            :return movements, captures, attacking:
        """
        movements = []
        captures = []
        attacking = []

        # Bishop moves diagonally, so we check all four diagonal directions
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                attacking.append((row, col))
                # There is a piece in the way
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                    else:
                        # Can capture piece but cannot move past it so exit loop
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                captures.append((row, col))
                        if isinstance(self.board[row][col], King):
                            attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                # Append empty squares to moves
                else:
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
                            movements.append((row, col))
                            attacking.append((row + diagonal_row, col + diagonal_col))

                row += diagonal_row
                col += diagonal_col

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

    def available_moves(self, testing_move):
        """
            Records valid moves available for the queen. The queen may move diagonally, horizontally,
            and vertically as long as there is not a piece in the way.
            :param testing_move:
            :return movements, captures, attacking:
        """
        movements = []
        captures = []
        attacking = []

        # Queen moves diagonally, so we check all four diagonal directions
        # Queen also moves horizontally and vertically
        counter = 0
        for diagonal_row, diagonal_col in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1)]:
            counter += 1
            row, col = self.current_row + diagonal_row, self.current_col + diagonal_col
            while 0 <= row < 8 and 0 <= col < 8:
                attacking.append((row, col))
                # There is a piece in the way
                if self.board[row][col] is not None:
                    if self.board[row][col].allegiance == self.allegiance:
                        attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                    else:
                        # Capture enemy piece or check king
                        if not testing_move:
                            if self.test_player_move((row, col), self.board):
                                captures.append((row, col))
                        if isinstance(self.board[row][col], King):
                            attacking.append((row + diagonal_row, col + diagonal_col))
                        break
                else:
                    if not testing_move:
                        if self.test_player_move((row, col), self.board):
                            movements.append((row, col))
                            attacking.append((row + diagonal_row, col + diagonal_col))

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

    def available_moves(self, testing_move):
        """
            Determines the King's valid moves. The King may move one square in any direction.
            :return movements, captures, attacking:
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

                row += move_row
                col += move_col

        # Check castle moves and add to available moves
        castle = self.castle()
        if castle is not None:
            for cas_row, cas_col, rook_col, new_rook_col in castle:
                attacking.append((cas_row, cas_col))
                if not self.under_attack(cas_row, cas_col):
                    movements.append((cas_row, cas_col))

        return movements, captures, attacking

    def castle(self):
        """
            Checks if castle move is possible for current piece. If so, it returns all
            valid castle moves to be added to the King's available moves. Otherwise, it
            returns None.
        """

        # If castle not possible
        if self.moves != 0 or self.current_col - 4 < 0 or self.current_col + 3 >= 8:
            return None

        # List to record valid castle moves
        castle_moves = []

        # Get corner squares adjacent to King
        left = self.board[self.current_row][self.current_col - 4]
        right = self.board[self.current_row][self.current_col + 3]

        row = self.current_row  # Row remains unchanged

        # Possible columns the king could move to
        left_none = self.current_col - 2
        left_rook = self.current_col - 4
        right_none = self.current_col + 2
        right_rook = self.current_col + 3

        # If there is a rook to the left
        if isinstance(left, Rook) and left.moves == 0 and left.allegiance == self.allegiance:
            # Squares between rook and king are empty
            if (self.board[self.current_row][self.current_col - 1] is None and
                    self.board[self.current_row][self.current_col - 2] is None
                    and self.board[self.current_row][self.current_col - 3] is None):
                # Returns column king will move to, the location of the rook, and the column rook will move to
                castle_moves.append((row, left_none, left_rook, left_none + 1))
                castle_moves.append((row, left_rook, left_rook, left_rook + 1))

        # If there is a rook to the right
        if isinstance(right, Rook) and right.moves == 0 and right.allegiance == self.allegiance:
            # Squares between rook and king are empty
            if (self.board[self.current_row][self.current_col + 1] is None and
                    self.board[self.current_row][self.current_col + 2] is None):
                castle_moves.append((self.current_row, right_none, right_rook, right_none - 1))
                castle_moves.append((self.current_row, right_rook, right_rook, right_rook - 1))

        if len(castle_moves) == 0:
            return None
        else:
            return castle_moves

    def __repr__(self):
        if self.allegiance == 'Black':
            return '♚'
        return '♔'
