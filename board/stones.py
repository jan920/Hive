from board.globals import FREE_SPACE, NUM_OF_CONNECTIONS, QUEEN, SPIDER, GRASSHOPPER, BEETLE, ANT, check_connection, check_position, count_new_position


class Stone:
    """Class representing stone in game Hive"""
    def __init__(self, colour, index, kind):
        self.colour = colour
        self.index = index
        self.connections = [FREE_SPACE] * NUM_OF_CONNECTIONS
        self.kind = kind
        self.position = None
        self.under = False
        self.above = False

    def __str__(self):
        """Prints stone as kind, index and colour, example B1W for beetle with index 1, colour white"""
        return self.kind + str(self.index) + self.colour

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        """Two stones are equal if their colour, kind and index are the same"""
        def condition1():
            return self.colour == other.colour

        def condition2():
            return self.kind == other.kind

        def condition3():
            return self.index == other.index

        if isinstance(other, str):
            return False
        elif condition1() and condition2() and condition3():
            return True
        else:
            return False

    def add_connection(self, position, connection):
        """Add new connection for self

        :param position: integer in range 0-5 stating position where connection to be added
        :param connection: either FREE_SPACE placeholder or another stone

        """
        self.connections[position] = connection

    def remove_connection(self, position):
        """Remove connection and replace it by FREE_SPACE placeholder
        :param position: integer in range 0-5 stating position where connection to be removed

        """

        self.connections[position] = FREE_SPACE

    def return_placing_moves(self, placing_positions):
        """Return possible moves how stone can be placed

        :param placing_positions: list of available positions where the stone can be placed
        :return: List of placing moves of class AvailMove

        """
        placing_moves = []
        for position in placing_positions:
            placing_moves.append(AvailMove(self, position))
        return placing_moves

    def is_movable(self):
        """Determine if stone is able to be moved

        :return: Boolean stating if stone is able to be moved according to the rules
        """
        def count_holes():
            holes = 0
            previous_connection_occupied = False
            for count in range(NUM_OF_CONNECTIONS+1):
                if self.connections[count%NUM_OF_CONNECTIONS] == FREE_SPACE:
                    if previous_connection_occupied:
                        holes += 1
                        previous_connection_occupied = False
                else:
                    previous_connection_occupied = True
            return holes

        def is_it_circle():
            """Determine if stone is part of circle"""
            def is_previous_space_free():
                """Return if previous connection on stone is free"""
                condition1 = check_connection(self, count-1, FREE_SPACE)
                return condition1

            def search_if_returns(c):
                track_positions = [self.connections[c]]
                closed_positions = [self]
                first_search = True
                #I must change it so it first runs all around self which are connected and then it continues
                while track_positions:
                    for c in range(NUM_OF_CONNECTIONS):
                        condition1 = track_positions[0].connections[c] == self
                        condition2 = not first_search
                        condition3 = track_positions[0].connections[c] != FREE_SPACE
                        condition4 = track_positions[0].connections[c] not in closed_positions
                        condition5 = track_positions[0] == self
                        if condition1 and condition2:
                            print("con1 and con2")
                            return True
                        elif not condition3:
                            first_search = False
                        elif condition3 and condition4:
                            track_positions.append(track_positions[0].connections[c])
                        elif condition5:
                            print('condition5 passed- track position is self')
                    else:
                        closed_positions.append(track_positions[0])
                        del track_positions[0]
                        first_search = False
                else:
                    print("run out of track_positions")
                    return False

            for count in range(NUM_OF_CONNECTIONS):
                if not check_connection(self, count, FREE_SPACE) and is_previous_space_free():
                    return search_if_returns(count)
            else:
                return True

        if self.above:
            return False
        elif self.under:
            return True
        else:
            free_positions = self.connections.count(FREE_SPACE)
            if free_positions == 0 or free_positions == 1 or free_positions == 5:
                return True
            elif count_holes() < 2:
                return True
            elif is_it_circle():
                return True
            else:
                return False

    def is_blocked(self):
        for c in range(NUM_OF_CONNECTIONS):
            cond1 = self.connections[c] == FREE_SPACE
            cond2 = self.connections[(c - 1) % NUM_OF_CONNECTIONS] == FREE_SPACE
            cond3 = self.connections[(c + 1) % NUM_OF_CONNECTIONS] == FREE_SPACE
            if cond1 and (cond2 or cond3):
                return False
        else:
            return True

    def basic_move(self, depth, game):

        def find_occupied_position(game, y, x):
            for i in range(NUM_OF_CONNECTIONS):
                if check_position(game, (y, x), i) != FREE_SPACE:
                    return i

        game.board[self.position[0]][self.position[1]] = FREE_SPACE
        possible_moves = [self.position]
        available_positions = []
        closed_positions = []
        d = 0
        while possible_moves:
            if d == depth:
                game.board[self.position[0]][self.position[1]] = self
                return available_positions
            count = 0
            y = possible_moves[0][0]
            x = possible_moves[0][1]
            i = find_occupied_position(game, y, x)
            for c in range(i, i + NUM_OF_CONNECTIONS + 1):
                if check_position(game, (y, x), c) == FREE_SPACE:
                    count += 1
                elif count > 1:
                    for c2 in [c - count, c - 1]:
                        next_position = count_new_position((y, x), c2)
                        if next_position not in closed_positions:
                            possible_moves.append(next_position)
                            condition1 = (d == 2 or depth != 3)
                            condition2 = next_position != self.position
                            condition3 = next_position not in available_positions
                            if condition1 and condition2 and condition3:
                                available_positions.append(next_position)
                    if count == 2 and c < i + 4:
                        count = 0
                    else:
                        break
                else:
                    count = 0
            closed_positions.append(possible_moves[0])
            del possible_moves[0]

            d += 1
        game.board[self.position[0]][self.position[1]] = self
        return available_positions


class Queen(Stone):
    """Inheriting from class stone with Queen abilities"""
    def __init__(self, colour, index):
        Stone.__init__(self, colour, index, kind=QUEEN)

    def __str__(self):
        return "Q " + self.colour

    def return_moves(self, game):
        available_moves = []
        if self.is_blocked():
            return available_moves
        else:
            available_positions = self.basic_move(1, game)
            for position in available_positions:
                available_moves.append(AvailMove(self, position))
        return available_moves


class Spider(Stone):
    """Inheriting from class stone with Spider abilities"""
    def __init__(self, colour, index):
        Stone.__init__(self, colour, index, kind=SPIDER)

    def return_moves(self, game):
        available_moves = []
        if self.is_blocked():
            return available_moves
        else:
            available_positions = self.basic_move(3, game)
            for position in available_positions:
                available_moves.append(AvailMove(self, position))
        return available_moves


class Grasshopper(Stone):
    """Inheriting from class stone with Grasshopper abilities"""

    def __init__(self, colour, index):
        Stone.__init__(self, colour, index, kind=GRASSHOPPER)

    def return_moves(self, game):
        available_moves = []
        for c in range(NUM_OF_CONNECTIONS):
            if self.connections[c] != FREE_SPACE:
                possible_position = self
                while possible_position.connections[c] != FREE_SPACE:
                    possible_position = possible_position.connections[c]
                else:
                    position = count_new_position(possible_position.position, c)
                    available_moves.append(AvailMove(self, position))
        return available_moves


class Beetle(Stone):
    """Inheriting from class stone with Beetle abilities"""
    def __init__(self, colour, index):
        Stone.__init__(self, colour, index, kind=BEETLE)

    def return_moves(self, game):
        available_moves = []
        if self.under:
            for c in range(NUM_OF_CONNECTIONS):
                position = count_new_position(self.position, c)
                available_moves.append(AvailMove(self, position))
        else:
            available_positions = self.basic_move(1, game)
            for position in available_positions:
                available_moves.append(AvailMove(self, position))
            for c in range(NUM_OF_CONNECTIONS):
                if self.connections[c] != FREE_SPACE:
                    position = count_new_position(self.position, c)
                    available_moves.append(AvailMove(self, position))
        return available_moves


class Ant(Stone):
    """Inheriting from class stone with Ant abilities"""
    def __init__(self, colour, index):
        Stone.__init__(self, colour, index, kind=ANT)

    def return_moves(self, game):
        available_moves = []
        if self.is_blocked():
            return available_moves
        else:
            available_positions = self.basic_move(100, game)

            for position in available_positions:
                available_moves.append(AvailMove(self, position))
        return available_moves


class AvailMove:
    """Class representing available move"""
    def __init__(self, stone, position):
        self.stone = stone
        self.position = position

    def __eq__(self, other):
        """Two moves are equal if the stones and positions of the moves are equal"""
        return self.stone == other.stone and self.position == other.position

    def __str__(self):
        return "stone " + str(self.stone) + " position " + str(self.position[0]) + " " + str(self.position[1])

    def __repr__(self):
        return self.__str__()
