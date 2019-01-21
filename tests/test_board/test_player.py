import sys

sys.path.append('../Hive/')

from board.player import Player

class TestPlayer():
    def test_create_player(self):
        player = Player("B")
        print(player)
        assert len(player.available_stones) == 11
