"""Global variables and functions shared over the whole module

Attributes:
    POSITIONS AROUND (list): list of tuples containing two integers,
    each of the tuples signifies difference in coordinates of different
    position around original position, first integer one is y difference
    in coordinate second integer is x difference in coordinate
    BEETLE (str): symbol for Beetle
    QUEEN (str): symbol for Queen
    SPIDER (str): symbol for Spider
    ANT (str): symbol for Ant
    GRASSHOPPER (str): symbol for Grasshopper
    NUM_OF_CONNECTIONS (int): number of possible connections each stone can have
    FREE_SPACE (str): character representing free space on board which cannot be ocupied
    PLACEHOLDER (str): character representing placeholder which can be replaced by stone
"""


POSITIONS_AROUND = [(-1, -1), (-1, 1), (0, 2), (1, 1), (1, -1), (0, -2)]

BEETLE = "B"

QUEEN = "Q"

SPIDER = "S"

ANT = "A"

GRASSHOPPER = "G"

NUM_OF_CONNECTIONS = 6

FREE_SPACE = '-'

PLACEHOLDER = '0'


def check_connection(stone, count, item):
    """Check if connection is equal to expected item"""
    return stone.connections[count % NUM_OF_CONNECTIONS] == item


def count_new_position(position, c):
    """Counts new position based on original position and integer
     choosing one of six positions around each position"""
    y_position = position[0]+POSITIONS_AROUND[c % NUM_OF_CONNECTIONS][0]
    x_position = position[1]+POSITIONS_AROUND[c % NUM_OF_CONNECTIONS][1]
    return y_position, x_position


def set_new_connection(game, stone, c):
    """
    Set new connection for stone based on position around
    stone, set that if that position is stone set it's
    position equal to stone received
    """

    position = count_new_position(stone.position, c)
    game.board[position[0]][position[1]].connections[(c+3) % NUM_OF_CONNECTIONS] = stone
    stone.connections[c % NUM_OF_CONNECTIONS] = game.board[position[0]][position[1]]


def check_position(game, position, c):
    """return content of position on board"""
    position = count_new_position(position, c)
    return game.board[position[0]][position[1]]
