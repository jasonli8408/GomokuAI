"""Main file of the Gomoku AI Project."""

import pygame
from pygame.colordict import THECOLORS
from project_game import GomokuGame
from ai import AIPlayer

_GRID_SIZE = 70
_MAX_STONE = 15
_MAX_WIDTH = _MAX_STONE * _GRID_SIZE
_MAX_HEIGHT = _MAX_STONE * _GRID_SIZE
_STONE_RADIUS = _GRID_SIZE // 2 - 3
SCREEN_SIZE = (_MAX_WIDTH, _MAX_HEIGHT)


def initialize_screen(screen_size: tuple[int, int], allowed: list) -> pygame.Surface:
    """Initialize pygame and the display window.

    allowed is a list of pygame event types that should be listened for while pygame is running.
    """
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(THECOLORS['white'])
    pygame.display.flip()

    pygame.event.clear()
    pygame.event.set_blocked(None)
    pygame.event.set_allowed([pygame.QUIT] + allowed)

    return screen


def run_visualization(game: GomokuGame) -> None:
    """Run the Gomoku visualization.

    Initialize a screen of the given size, and show the grid when show_grid is True.

    This function is provided for you for Part 3, and you *should not change it*.
    Instead, your task is to implement the helper function handle_mouse_click (and
    any other helpers you decide to add).
    """
    # Initialize the Pygame screen, allowing for mouse click events.
    screen = initialize_screen((_MAX_WIDTH, _MAX_HEIGHT), [pygame.MOUSEBUTTONDOWN])
    while True:
        # Draw the list (on a white background)
        screen.fill(THECOLORS['gray'])  # change to yellow
        game.draw_background(screen)
        game.draw_stone(screen)
        pygame.display.flip()

        # Wait for an event (either pygame.MOUSEBUTTONDOWN or pygame.QUIT)
        event = pygame.event.wait()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Call our event handling method
            if game.count_stones() % 2 == 0:
                handle_mouse_click(game, event)
            else:
                ai_player = AIPlayer(game)
                game.make_move(ai_player.activate_make_move(game)[1])
        if game.get_winner() == 'White':
            game.draw_stone(screen)
            font2 = pygame.font.SysFont('SimHei', 150)
            fwidth, fheight = font2.size('White Wins!')
            _print_text(screen, font2, (1050 - fwidth) // 2, (1050 - fheight) // 2,
                        'White Wins!', (255, 0, 0))
            pygame.display.update()
            pygame.time.wait(3000)
            print('White Wins!')
            break
        elif game.get_winner() == 'Black':
            print('Black Wins!')
            game.draw_stone(screen)
            font2 = pygame.font.SysFont('SimHei', 150)
            fwidth, fheight = font2.size('Black Wins!')
            _print_text(screen, font2, (1050 - fwidth) // 2, (1050 - fheight) // 2,
                        'Black Wins!', (255, 0, 0))
            pygame.display.update()
            pygame.time.wait(3000)
            break

    pygame.display.quit()


def _print_text(screen: pygame.Surface, font: pygame.font.SysFont, x: int, y: int, text: str,
                fcolor: tuple[int, int, int] = (255, 255, 255)) -> None:
    """helper function that prints the winner on the game board the game ends."""
    img_text = font.render(text, True, fcolor)
    screen.blit(img_text, (x, y))


def handle_mouse_click(game: GomokuGame, event: pygame.event.Event) -> None:
    """Handle a mouse click event.

    A pygame mouse click event object has two attributes that are important for this method:
        - event.pos: the (x, y) coordinates of the mouse click
        - event.button: an int representing which mouse button was clicked.
                        1: left-click, 3: right-click

    The screen_size is a tuple of (width, height), and should be used together with
    event.pos to determine which cell is being clicked. If a click happens exactly on
    the boundary between two cells, you may decide which cell is selected.

    Preconditions:
        - event.type == pygame.MOUSEBUTTONDOWN
        - screen_size[0] >= 200
        - screen_size[1] >= 200
    """
    if event.button == 1:
        game.make_move((event.pos[0] // _GRID_SIZE, event.pos[1] // _GRID_SIZE))


if __name__ == '__main__':
#     import python_ta.contracts
#     python_ta.contracts.check_all_contracts()
#
#     import doctest
#     doctest.testmod()
#
#     import python_ta
#     python_ta.check_all(config={
#         'max-line-length': 100,
#         'disable': ['E1136', 'E9998', 'R0913', 'E1101'],
#         'extra-imports': ['pygame', 'project_game', 'pygame.colordict', 'ai'],
#         'max-nested-blocks': 4
#     })

    while True:
        print('-' * 40,
              '\nWelcome to the Gomoku Game!')
        option = input('\033[33mEnter go to start the game...\033[0m\n')
        if option != 'go':
            print('\033[31mInvalid option\033[0m')
        else:
            start_game = GomokuGame()
            run_visualization(start_game)
