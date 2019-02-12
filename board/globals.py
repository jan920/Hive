"""Global variables and functions shared over the whole module"""


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
    """Counts new position based on original position and integer choosing one of six positions around each position"""
    y = position[0]+POSITIONS_AROUND[c % NUM_OF_CONNECTIONS][0]
    x = position[1]+POSITIONS_AROUND[c % NUM_OF_CONNECTIONS][1]
    return y, x


def set_new_connection(game, stone, c):
    """
    Set new connection for stone based on position around stone, set that if that position is stone set it's
    position equal to stone received
    """

    position = count_new_position(stone.position, c)
    game.board[position[0]][position[1]].connections[(c+3) % NUM_OF_CONNECTIONS] = stone
    stone.connections[c] = game.board[position[0]][position[1]]


def check_position(game, position, c):
    """return content of position on board"""
    position = count_new_position(position, c)
    return game.board[position[0]][position[1]]
