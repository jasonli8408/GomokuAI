"""
The file used to represent the game board and game state of Gomoku.
"""

from __future__ import annotations
from typing import Optional
import copy
import pygame

################################################################################
# Representing Gomoku Game
################################################################################
_MAX_MOVES = 15 * 15
_DIRECTIONS = [[(-1, 0), (1, 0)], [(0, -1), (0, 1)], [(-1, 1), (1, -1)], [(-1, -1), (1, 1)]]
_GRID_SIZE = 70
_MAX_STONE = 15
_MAX_WIDTH = _MAX_STONE * _GRID_SIZE
_MAX_HEIGHT = _MAX_STONE * _GRID_SIZE
_STONE_RADIUS = _GRID_SIZE // 2 - 3
_WHITE = (255, 255, 255)
_BLACK = (0, 0, 0)
_RED = (255, 23, 140)

_CHESS_PATTERN_BLACK = {'Connect_Five': [2, 2, 2, 2, 2],
                        'STOP_FOUR': [1, 1, 1, 1, 2],
                        'STOP_THREE': [0, 1, 1, 1, 2],
                        'STOP_THREE_2': [2, 1, 1, 1, 2],
                        'Open_Four': [0, 2, 2, 2, 2, 0],
                        'Dead_Four': [2, 2, 2, 2],
                        'Blocked_Four_4': [2, 1, 1, 1, 1, 2],
                        'Blocked_Four_1': [0, 2, 2, 2, 2, 1],  # [2, 1, 1, 1, 1, 0] flip
                        'Blocked_Four_2': [2, 2, 2, 0, 2],  # 1,0,1,1,1 flip
                        'Blocked_Four_3': [2, 2, 0, 2, 2],
                        'Open_Three_1': [0, 2, 2, 2, 0],
                        'Open_Three_2': [2, 0, 2, 2],  # 1 1 0 1 flip
                        'Pattern_Three_1': [0, 0, 2, 2, 2, 1],  # flip
                        'Pattern_Three_2': [0, 2, 0, 2, 2, 1],  # flip
                        'Pattern_Three_3': [0, 2, 2, 0, 2, 0],  # flip
                        'Pattern_Three_4': [2, 0, 0, 2, 2],
                        'Pattern_Three_5': [2, 0, 2, 0, 2],
                        'Pattern_Three_6': [1, 0, 2, 2, 2, 0, 1],
                        'Pattern_Two_1': [0, 0, 2, 2, 0, 0],
                        'Pattern_Two_2': [0, 2, 0, 2, 0],
                        'Pattern_Two_3': [2, 0, 0, 2],
                        'Lian_4': [1, 1, 2, 1],
                        'Live_3_kong_1': [1, 0, 2, 2, 2, 2],
                        'black_win2': [1, 2, 2, 2, 2, 2],
                        'black_win': [1, 2, 2, 2, 2, 2, 1]}

_CHESS_PATTERN_SCORE = {'Connect_Five': 99999990,  # BBBBB
                        'black_win': 99999980,      # WBBBBB
                        'black_win2': 99999970,     # wbbbbbw
                        'Blocked_Four_4': 88888880,  # BWWWWB
                        'STOP_THREE_2': 77777770,  # BWWWB
                        'Lian_4': 77777780,
                        'Open_Four': 80000000,  # 0BBBB0
                        'STOP_FOUR': 10000000,
                        'STOP_THREE': 77777780,
                        'Live_3_kong_1': 71000,
                        'Blocked_Four_1': 60000,  # [2, 1, 1, 1, 1, 0] flip
                        'Blocked_Four_2': 55000,  # 1,0,1,1,1 flip
                        'Blocked_Four_3': 55000,
                        'Dead_Four': 20000,         # BBBB
                        'Open_Three_1': 50000,
                        'Open_Three_2': 30000,  # 1 1 0 1 flip
                        'Pattern_Three_1': 10000,  # flip
                        'Pattern_Three_2': 8000,  # flip
                        'Pattern_Three_3': 8000,  # flip
                        'Pattern_Three_4': 9000,
                        'Pattern_Three_5': 6000,
                        'Pattern_Three_6': 8000,
                        'Pattern_Two_1': 2000,
                        'Pattern_Two_2': 1500,
                        'Pattern_Two_3': 1000}


class GomokuGame:
    """A class representing a state of a game of Gomoku, as well as visualization of the game.
    """
    # Private Instance Attributes:
    #   - _board: a two-dimensional representation of a Gomoku board, where each position is 0,
    #             1 or 2: 0 if empty, 1 if white stone, 2 if black stone
    #   - _valid_moves: a list of the valid moves of the current player
    #   - _is_white_active: a boolean representing whether white is the current player
    #   - _move_count: the number of moves that have been made in the current game
    #   - _moves_so_far: keep track of all the moves so far
    #   - _last_move: record the location of the latest move.
    #   - _width: the width of the visualization
    #   - _height: the height of the visualization
    _board: list[list[int]]
    _valid_moves: list[tuple[int, int]]
    _is_white_active: bool
    _move_count: int
    _moves_so_far: list[tuple[int, int]]
    last_move: Optional[tuple[int, int]]
    _width: int
    _height: int

    def __init__(self, board: list[list[int]] = None, white_active: bool = True,
                 move_count: int = 0, width: int = 15, height: int = 15) -> None:
        """Initialize the game state of Gomoku game."""

        lst = []
        for _ in range(0, 15):
            sublist = []
            for _ in range(0, 15):
                sublist.append(0)
            lst.append(sublist)
        self._board = lst
        if board:
            self._board = board
        self._is_white_active = white_active
        self._move_count = move_count
        self._valid_moves = [(y, x) for x in range(0, 15) for y in range(0, 15)]
        self._moves_so_far = []
        self.last_move = None
        self._width = width
        self._height = height

    def get_board(self) -> list[list[int]]:
        """literally get the board"""
        return self._board

    def count_stones(self) -> int:
        """Count number of stones on the game board."""
        return self._move_count

    def return_existing_moves(self) -> list[tuple[int, int]]:
        """Return a list of the existing moves made by both players."""
        return self._moves_so_far

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Return a list of the valid moves for the active player."""
        return self._valid_moves

    def make_move(self, move: tuple[int, int]) -> None:
        """Make the given stone move. This instance of Gomoku will be mutated, and will
        afterwards represent the game state after move is made. Move is represented by
        a tuple of (y_coordinate, x_coordinate) of the game board. Note that the origin
        coordinate, i.e. (0, 0), is on the top left corner of the game board instead of
        bottom left like a Cartesian plane.

        If move is not a currently valid move, raise a ValueError.
        """
        if move not in self._valid_moves:
            print(f'Move "{move}" is not valid')
        else:
            self._board = self._board_after_move(move)
            self._is_white_active = not self._is_white_active
            self._move_count += 1
            self.last_move = move
            self._moves_so_far.append(move)
            self._valid_moves.remove(move)

    def copy_and_make_move(self, move: tuple[int, int]) -> Optional[GomokuGame]:
        """Make the given stone move in a copy of this GomokuGame, and return that copy.

        If move is not a currently valid move, raise a ValueError.
        """
        if move not in self._valid_moves:
            print(f'Move "{move}" is not valid')
            return None
        else:
            c = GomokuGame(board=copy.deepcopy(self._board),
                           white_active=self._is_white_active,
                           move_count=self._move_count)
            c.make_move(move)
            return c

    def _board_after_move(self, move: tuple[int, int]) -> list[list[int]]:
        """Return the board state given a valid move."""
        if self._is_white_active:
            # a white stone has been placed
            self._board[move[0]][move[1]] = 1
        else:
            # a black stone has been placed
            self._board[move[0]][move[1]] = 2

        return self._board

    def is_white_move(self) -> bool:
        """Return whether the white player is to move next."""
        return self._is_white_active

    def get_winner(self) -> Optional[str]:
        """Return the winner of the game (black or white) or 'draw' if the game ended in a draw.

        Return None if the game is not over.
        """
        if self._move_count == 0:
            return None
        y_coordinate = self.last_move[0]
        x_coordinate = self.last_move[1]
        if self._move_count >= _MAX_MOVES:
            return 'Draw'
        elif self._five_in_a_row(y_coordinate, x_coordinate, self._is_white_active):
            return 'Black' if self._is_white_active else 'White'
        else:
            return None

    def _five_in_a_row(self, y_coordinate: int, x_coordinate: int, white_turn: bool) -> bool:
        """Return whether a type of stone formed 5 in a row. Here, elements in sublist of
        _DIRECTIONS is represented as (x_direction, y_direction), which is different
        representation than before when representing moves as (y_coordinate, x_coordinate).

        Note: count must be exactly 5 in order to win. In cases there's a move that
        results in a row of more than 5 stones, which doesn't count as a win.
        """
        for direction in _DIRECTIONS:
            count = 1
            for (x_direction, y_direction) in direction:
                count += self._count_direction_5(y_coordinate, x_coordinate,
                                                 x_direction, y_direction, white_turn)
                if count == 5:
                    return True

        return False

    def _count_direction_5(self, y_coordinate: int, x_coordinate: int,
                           x_direction: int, y_direction: int, white_turn: bool) -> int:
        """Count number of stones of same color formed given a direction."""
        if white_turn:
            want = 2
        else:
            want = 1

        count = 0
        for step in range(1, 5):
            if x_direction != 0 and (x_coordinate + x_direction * step < 0
                                     or x_coordinate + x_direction * step > 14):
                break
            elif y_direction != 0 and (y_coordinate + y_direction * step < 0
                                       or y_coordinate + y_direction * step > 14):
                break
            elif self._board[y_coordinate + y_direction * step][x_coordinate + x_direction * step] \
                    == want:
                count += 1
            else:
                break
        return count

################################################################################
# Draw the game board on pygame
################################################################################

    def printing_board(self) -> None:
        """A simple visualization of the Gomoku game. Print out the board visually in the console,
        where @ represents white stones and # represents black stones,

        This can be used to check Errors."""
        str_board = []
        for i in range(0, 15):
            sublist = []
            for j in range(0, 15):
                if self._board[i][j] == 1:
                    sublist.append('@')
                elif self._board[i][j] == 2:
                    sublist.append('#')
                else:
                    sublist.append(' ')
            str_board.append(sublist)

        for i in range(0, 15):
            print(' -- '.join(str_board[i]))

    def draw_stone(self, screen: pygame.Surface) -> None:
        """Draw the stones using pygame."""
        font = pygame.font.SysFont("arial", _GRID_SIZE * 2 // 4)
        # draw the outline of each move
        if len(self._moves_so_far) > 0:
            last_move = self._moves_so_far[-1]
            x_index, y_index, width, height = _each_unit_grid(last_move[0], last_move[1])
            pygame.draw.lines(screen, _RED, True, [(x_index, y_index), (x_index + width, y_index),
                                                   (x_index + width, y_index + height),
                                                   (x_index, y_index + height)], 2)

        # draw the stone and denote the number of stones on each stone
        moves = self._moves_so_far
        for i in range(0, len(moves)):
            x_index, y_index, width, height = _each_unit_grid(moves[i][0], moves[i][1])
            stone_radius = _STONE_RADIUS
            position = (x_index + width // 2, y_index + height // 2)  # center of the circle
            if self._board[moves[i][0]][moves[i][1]] == 1:
                pygame.draw.circle(screen, _WHITE, position, stone_radius)
                number = font.render(str(i + 1), True, _BLACK)
                number_rect = number.get_rect()
                number_rect.center = position
                screen.blit(number, number_rect)
            else:
                pygame.draw.circle(screen, _BLACK, position, stone_radius)
                number = font.render(str(i + 1), True, _WHITE)
                number_rect = number.get_rect()
                number_rect.center = position
                screen.blit(number, number_rect)

    def draw_background(self, screen: pygame.Surface) -> None:
        """Draw the whole game board of this game. """
        color = (0, 0, 0)
        # draw four small points that the Gomoku board needs
        rec_size = 10
        position = [(3, 3), (11, 3), (3, 11), (11, 11), (7, 7)]
        for (i, j) in position:
            pygame.draw.rect(screen, color, (_GRID_SIZE // 2 + i * _GRID_SIZE - rec_size // 2,
                                             _GRID_SIZE // 2 + j * _GRID_SIZE - rec_size // 2,
                                             rec_size, rec_size))

        for j in range(self._width):
            # draw a horizontal line
            start_position = (_GRID_SIZE // 2 + _GRID_SIZE * j, _GRID_SIZE // 2)
            end_position = (_GRID_SIZE // 2 + _GRID_SIZE * j, _MAX_HEIGHT - _GRID_SIZE // 2)
            if j == self._width // 2:
                width = 3
            else:
                width = 1
            pygame.draw.line(screen, color, start_position, end_position, width)

        for i in range(self._height):
            # draw a horizontal line
            start_position = (_GRID_SIZE // 2, _GRID_SIZE // 2 + _GRID_SIZE * i)
            end_position = (_MAX_WIDTH - _GRID_SIZE // 2, _GRID_SIZE // 2 + _GRID_SIZE * i)
            if i == self._height // 2:
                width = 3
            else:
                width = 1
            pygame.draw.line(screen, color, start_position, end_position, width)

################################################################################
# Evaluate function
################################################################################

    def evaluate_game(self) -> int:
        """
        Return the evaluated score of the current game.
        """
        center = self.last_move
        score = 0
        for direction in [0, 1, 2, 3]:
            old_line, new_line = self.generate_line(center, direction)
            score += _evaluate_line(new_line) - _evaluate_line(old_line)
        return score


    def generate_line(self, center: tuple[int, int], direction: int) -> any:
        """Return a list of pieces on the line that passes through the given position in the given
        direction.

        """
        def getline(board: any) -> any:
            """inner function that return a list"""

            if direction == 0:
                return board[center[0]]
            if direction == 1:
                return [lst[center[1]] for lst in board]
            if direction == 2:

                x = [lst[center[1] + i - center[0]] if center[1] + i - center[0] >= 0 and center[
                    1] + i - center[0] <= 14 else -1 for i, lst in enumerate(board)]
                return list(filter(lambda a: a != -1, x))
            if direction == 3:
                x = [
                    lst[center[0] - i + center[1]] if center[0] - i + center[1] >= 0 and center[
                        0] - i + center[1] <= 14 else -1 for i, lst in enumerate(board)]
                return list(filter(lambda a: a != -1, x))
            return None
        oldboard = copy.deepcopy(self._board)
        oldboard[center[0]][center[1]] = 0
        return getline(oldboard), getline(self._board)

    def valid_moves_with_neighbour(self, radius: int = 1) -> list:
        """
        Return valid moves in the current game that have already placed piece surrounding it.
        """
        valid_moves_with_neighbour = []
        for move in self._valid_moves:
            if self._check_neighbour(move, radius):
                valid_moves_with_neighbour.append(move)

        return valid_moves_with_neighbour

    def _check_neighbour(self, move: tuple[int, int], radius: int = 2) -> bool:
        """Return whether there exists a existing stone that neighbours
        the given move on the game board.
        """
        y_1, y_2 = move[0] - radius, move[0] + radius
        x_1, x_2 = move[1] - radius, move[1] + radius

        for y in range(y_1, y_2 + 1):
            for x in range(x_1, x_2 + 1):
                if 0 <= y <= 14 and 0 <= x <= 14:
                    if self._board[y][x] != 0:
                        return True
        return False


# helper functions out side of the class below:
def _each_unit_grid(x_axis: int, y_axis: int) -> list:
    """Return the particular grid's position with its length and width. """
    x_coordinate = x_axis * _GRID_SIZE
    y_coordinate = y_axis * _GRID_SIZE
    return [x_coordinate, y_coordinate, _GRID_SIZE, _GRID_SIZE]


def _evaluate_line(line: list[int]) -> int:
    """Return the evaluate score given a line of inputs"""
    score = 0
    pattern = _CHESS_PATTERN_BLACK

    for key in pattern:
        a_1 = pattern[key]
        a_2 = pattern[key][::-1]
        b = line
        if _check_contain(a_1, b) or _check_contain(a_2, b):
            score += _CHESS_PATTERN_SCORE[key]
    return score


def _check_contain(a: list[int], b: list[int]) -> bool:
    """Return if list B contains list A."""
    n = len(a)
    return any(a == b[i:i + n] for i in range(len(b) - n + 1))


# if __name__ == '__main__':
#     import python_ta.contracts
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'disable': ['E1136', 'E9998', 'R0913', 'R0902'],
#         'extra-imports': ['pygame', 'project_game', 'copy', 'typing'],
#         'max-nested-blocks': 4
#     })
