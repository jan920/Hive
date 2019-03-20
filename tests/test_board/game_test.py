import sys

sys.path.append('../Hive/')

from board.game import create_board, Game


class TestGame():
    def test_create_board_passes(self):
        print(create_board(64))

    def test_create_game_passes(self):
        game = Game()

    def test_print_game_passes(self):
        game = Game()
        print(game)
