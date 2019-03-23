import sys

import pytest

sys.path.append('../Hive/')

from board.globals import check_connection, count_new_position, \
    set_new_connection, check_position

from board.stones import Stone

from board.game import Game


class TestCheckConnection:

    def setup_method(self):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        self.Stone_1 = Stone("B", 0, "Q")
        self.Stone_2= Stone("W", 0, "Q")
        self.Stone_1.connections = ["-", self.Stone_2, "0", 3, 4, 5]

    def test_correct_item(self):
        assert check_connection(self.Stone_1, 0, "-") is True
        assert check_connection(self.Stone_1, 1, self.Stone_2) is True
        assert check_connection(self.Stone_1, 6, "-") is True
        assert check_connection(self.Stone_1, 7, self.Stone_2) is True

    def test_incorrect_item(self):
        assert check_connection(self.Stone_1, 0, self.Stone_1) is False
        assert check_connection(self.Stone_1, 1, 3) is False
        assert check_connection(self.Stone_1, 6, "0") is False
        assert check_connection(self.Stone_1, 7, "-") is False


class TestCountNewPosition:
    def test_correct_position(self):
        assert count_new_position((10, 10), 0) == (9, 9)
        assert count_new_position((10, 10), 1) == (9, 11)
        assert count_new_position((10, 10), 2) == (10, 12)
        assert count_new_position((10, 10), 3) == (11, 11)
        assert count_new_position((10, 10), 4) == (11, 9)
        assert count_new_position((10, 10), 5) == (10, 8)
        assert count_new_position((10, 10), 6) == (9, 9)

    def test_incorrect_position(self):
        assert count_new_position((10, 10), 0) != (9, 10)
        assert count_new_position((10, 10), 1) != (9, 10)
        assert count_new_position((10, 10), 2) != (10, 10)
        assert count_new_position((10, 10), 3) != (11, 10)
        assert count_new_position((10, 10), 4) != (11, 10)
        assert count_new_position((10, 10), 5) != (10, 10)


class TestSetNewConnection:
    def setup_method(self):
        self.game = Game()
        self.Stone_1 = Stone("B", 0, "Q")
        self.Stone_2 = Stone("W", 0, "Q")
        self.Stone_3 = Stone("B", 1, "Q")
        self.Stone_4 = Stone("W", 1, "Q")

        self.Stone_1.position = (34, 34)
        self.game.board[34][36] = self.Stone_2
        self.game.board[34][32] = self.Stone_3
        self.game.board[35][35] = self.Stone_4

    def test_correct_connection(self):
        set_new_connection(self.game, self.Stone_1, 2)
        set_new_connection(self.game, self.Stone_1, 5)
        set_new_connection(self.game, self.Stone_1, 9)

        assert self.Stone_1.connections[2] is self.Stone_2
        assert self.Stone_1.connections[5] is self.Stone_3
        assert self.Stone_1.connections[3] is self.Stone_4


    '''
    def set_new_connection(game, stone, c):
        """
        Set new connection for stone based on position around
        stone, set that if that position is stone set it's
        position equal to stone received
        """

        position = count_new_position(stone.position, c)
        game.board[position[0]][position[1]].connections[(c + 3) % NUM_OF_CONNECTIONS] = stone
        stone.connections[c] = game.board[position[0]][position[1]]
    '''


class TestCheckPosition:

    def setup_method(self):
        self.game = Game()
        self.Stone_1 = Stone("B", 0, "Q")

        self.game.board[1][1] = 1
        self.game.board[2][2] = 2
        self.game.board[3][3] = self.Stone_1
        """return content of position on board
        position = count_new_position(position, c)
        return game.board[position[0]][position[1]]
        """

    def test_correct_position(self):
        assert check_position(self.game, (10, 10), 1) is "0"
        assert check_position(self.game, (1, 3), 5) is 1
        assert check_position(self.game, (2, 0), 2) is 2
        assert check_position(self.game, (3, 5), 11) is self.Stone_1

    def test_incorrect_position(self):
        assert check_position(self.game, (10, 10), 3) is not "-"
        assert check_position(self.game, (9, 10), 2) is not "0"
