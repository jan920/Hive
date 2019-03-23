class AvailMove:
    """Class representing available move"""
    def __init__(self, stone, position):
        self.stone = stone
        self.position = position

    def __eq__(self, other):
        """Two moves are equal if the stones and positions of the moves are equal"""
        return self.stone == other.stone and self.position == other.position

    def __str__(self):
        return "stone " \
               + str(self.stone) \
               + " position " \
               + str(self.position[0]) + " " \
               + str(self.position[1])

    def __repr__(self):
        return self.__str__()
