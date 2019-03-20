from board.globals import QUEEN, SPIDER, GRASSHOPPER, BEETLE, ANT

from board.stones import Spider, Beetle, Grasshopper, Ant, Queen


class Player:
    """Class representing player in game Hive"""
    def __init__(self, colour, choice_of_stones=(QUEEN, SPIDER, GRASSHOPPER, BEETLE, ANT)):
        self.colour = colour
        self.queen = False
        self.placed_stones = []
        self.available_stones = []
        for stone in choice_of_stones:
            if stone is SPIDER:
                for count in range(2):
                    self.available_stones.append(Spider(colour, count))
            elif stone is BEETLE:
                for count in range(2):
                    self.available_stones.append(Beetle(colour, count))
            elif stone is GRASSHOPPER:
                for count in range(3):
                    self.available_stones.append(Grasshopper(colour, count))
            elif stone is ANT:
                for count in range(3):
                    self.available_stones.append(Ant(colour, count))
            else:
                self.available_stones.append(Queen(colour, 1))

    def __repr__(self):
        if self.colour == "B":
            return "Second player"

        return "First player"

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    pass
