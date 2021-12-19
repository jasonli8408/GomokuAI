"""
The file used to represent AIPlayer of the game Gomoku.
"""
from typing import Optional
import project_game


class AIPlayer:
    """A Gomoku player that plays using scores evaluated from current game board.

    Instance Attributes:
        - _game: the current game the player needs to make a move with
        - _next_move: the move the player is going to play
        - _depth: the number of layers the make_move functions wants to recurse on
        to explore possible moves
    """
    _game: project_game.GomokuGame
    _next_move: Optional[tuple[int, int]]
    _depth: Optional[int]

    def __init__(self, game: project_game.GomokuGame, depth: Optional[int] = 4) -> None:
        """Initialize this player.
        """
        self._game = game
        self._next_move = None
        self._depth = depth

    def make_move(self, game: project_game.GomokuGame,
                  d: int) -> int:
        """Return the alpha value from alpha beta pruning in this function.
        Assign self._next_move.
        """
        self._next_move = None  # reset to None
        next_move = None

        if game.last_move is None:
            next_move = (7, 7)  # when first, always plays center
            self._next_move = next_move
            score = 100
            return score
        else:
            score = game.evaluate_game()  # evaluate current game

        if d == 0:
            # or abs(score) >= 1000000
            score = game.evaluate_game()
            return score

        # restrict possible moves to more relevant ones with neighbour
        possible_moves = game.valid_moves_with_neighbour()

        if len(possible_moves) == 0:
            return score

        score = 0
        for move in possible_moves:
            new_game = game.copy_and_make_move(move)

            # score is multiplied with -1 to make codes more efficient,
            # so we are always finding the maximum value for either min or max layer

            x = self.make_move(new_game, d - 1)  # recursion happens here
            if x >= score:
                score = x
                next_move = move

        # if d == self._depth:  # and next_move
            # assert next_move is not None
        self._next_move = next_move  # this is the best move

        return score

    def make_move_and_prune(self, game: project_game.GomokuGame, d: int,
                            alpha: float = float('-inf'), beta: float = float('inf')) -> int:
        """Return the alpha value from alpha beta pruning in this function.
        Assign self._next_move.
        """
        self._next_move = None  # reset to None
        next_move = None

        if game.last_move is None:
            next_move = (7, 7)  # when first, always plays center
            self._next_move = next_move
            score = 100
            return score
        else:
            score = game.evaluate_game()  # evaluate current game

        if d == 0:
            # or abs(score) >= 1000000
            score = game.evaluate_game()
            return score

        # restrict possible moves to more relevant ones with neighbour
        possible_moves = game.valid_moves_with_neighbour()

        if len(possible_moves) == 0:
            return score

        for move in possible_moves:
            new_game = game.copy_and_make_move(move)

            # score is multiplied with -1 to make codes more efficient,
            # so we are always finding the maximum value for either min or max layer
            # recursion happens here
            score = - self.make_move_and_prune(new_game, d - 1, -beta, -alpha)

            if score > alpha:
                alpha = score
                next_move = move  # save the best move so far
                if alpha >= beta:  # pruning condition met
                    break

        if d == self._depth:  # and next_move
            assert next_move is not None
            self._next_move = next_move  # this is the best move

        return alpha

    def activate_make_move(self, game: project_game.GomokuGame,
                           d: int = 1) -> tuple[int, tuple[int, int]]:
        """Return a tuple with score of the game with decided move and the decided move.
        Call make_mov function.
        """
        self._depth = d
        self._next_move = None
        score = self.make_move(game, d)
        return score, self._next_move


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
#         'disable': ['E1136'],
#         'extra-imports': ['typing', 'project_game'],
#         'max-nested-blocks': 4
#     })
