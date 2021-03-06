from random import randint

from board.globals import FREE_SPACE, PLACEHOLDER, set_new_connection, check_position, \
                          NUM_OF_CONNECTIONS, BEETLE, QUEEN, count_new_position

from board.player import Player

from board.available_move import AvailMove


class Game:
    """Class representing game of Hive"""
    def __init__(self, turn=1, size=68, board=None, placed_stones=[]):
        self.turn = turn
        self.size = size
        if board:
            self.board = board
        else:
            self.board = create_board(size)
        self.placed_stones = placed_stones

    def __str__(self):
        """Prints the board"""
        def find_first_stone_from_top():
            """Find first line which contains stone"""
            for y_position in range(self.size):
                for item in self.board[y_position]:
                    if item not in [PLACEHOLDER, FREE_SPACE]:
                        return y_position
            return 0

        def find_first_stone_from_bottom():
            """Find last line which contains stone"""
            for y_position in reversed(range(self.size)):
                for item in self.board[y_position]:
                    if item not in [PLACEHOLDER, FREE_SPACE]:
                        return y_position
            return self.size - 1

        def find_first_left_right():
            """"Find left, right most position of stone, withing area
            limited by top, bottom arguments received"""
            left = self.size
            right = 0
            for y_position in range(top, bottom + 1):
                for counter, item in enumerate(self.board[y_position]):
                    if item not in [PLACEHOLDER, FREE_SPACE]:
                        if counter < left:
                            left = counter
                        if counter > right:
                            right = counter
            return left, right

        top = find_first_stone_from_top()

        bottom = find_first_stone_from_bottom()

        most_left, most_right = find_first_left_right()

        if most_left == self.size and most_right == 0:
            res = "No stones have been placed so far"
        else:
            res = "   "
            for x_position in range(most_left-2, most_right+3):
                res += str(x_position)
                if x_position < 10:
                    res += "  "
                else:
                    res += " "
            for y_position in range(top-1, bottom+2):
                res += "\n"
                res += str(y_position)
                res += " "
                for x_position in range(most_left-2, most_right+3):
                    if self.board[y_position][x_position] == FREE_SPACE:
                        res += " {} ".format(FREE_SPACE)
                    elif self.board[y_position][x_position] == PLACEHOLDER:
                        res += " {} ".format(PLACEHOLDER)
                    else:
                        res += str(self.board[y_position][x_position])
            res += "\n"

        return res

    def __repr__(self):
        return self.__str__()


def is_game_terminal(player1, player2):
    """Return boolean if game is terminal"""
    if is_players_queen_surrounded(player1):
        if is_players_queen_surrounded(player2):
            print("its a tie")
            return True
        print("player 1 lost")
        return True
    if is_players_queen_surrounded(player2):
        print("player 2 lost")
        return True
    return False


def create_board(size):

    """Create board

    Params:
    size: positive integer stating size of the board
    Returns:
    return created board
    Raises
    ValueError: if size is not integer

    """

    board = []
    for y_position in range(size):
        board.append([])
        for x_position in range(size):
            if x_position % 2 == y_position % 2:
                board[y_position].append(PLACEHOLDER)
            else:
                board[y_position].append(FREE_SPACE)
    return board


def is_players_queen_surrounded(player):
    """Return boolean if queen is surrounded"""
    if player.queen:
        return player.queen.connections.count(PLACEHOLDER) == 0
    return False


def create_game(size=64, stones=()):
    """Create game from received stones

    :param size: positive integer stating size of the board for the game
    :param stones: list of stones
    :return: created game
    :raise
    ValueError: if size not integer
    ValueError: if stones are not stone class, miss property position
    ValueError: if stones position is not correct

    """

    game = Game(turn=1, size=size, board=None, placed_stones=[stones])

    for stone in stones:
        if stone.position[0] % 2 == stone.position[1] % 2:
            game.board[stone.position[0]][stone.position[1]] = stone
            make_connections(stone, game)

        else:
            raise ValueError('stone stone position ')


def find_available_moves(player, game):
    def return_placing_positions():
        def check_placable(position):
            if game.board[position[0]][position[1]] == PLACEHOLDER:
                for index in range(NUM_OF_CONNECTIONS):
                    condition1 = check_position(game, position, index) == PLACEHOLDER
                    condition2 = check_position(game, position, index) in player.placed_stones
                    if not condition1 and not condition2:
                        return []
                return position
            return []

        placing_positions = set()
        for stone in player.placed_stones:
            for index in range(NUM_OF_CONNECTIONS):
                possible_position = count_new_position(stone.position, index)
                if check_placable(possible_position):
                    placing_positions.add(possible_position)
        return placing_positions

    def return_placing_moves():
        """Return all possible moves how stones could be placed"""
        placing_moves = []
        placing_positions = return_placing_positions()
        for stone in player.available_stones:
            placing_moves += stone.return_placing_moves(placing_positions)
        return placing_moves

    def first_second_turn():
        """Return all possible moves in first and second turn"""
        first_turn_moves = []
        if game.turn == 1:
            position = (34, 34)
        else:
            position = (34, 36)
        for stone in player.available_stones:
            if stone.kind != QUEEN:
                first_turn_moves.append(AvailMove(stone, position))
        return first_turn_moves

    def queen_placed():
        """Return all possible moves after queen has been moved which makes pieces movable"""
        if player.available_stones:
            queen_placed_moves = return_placing_moves()
        else:
            queen_placed_moves = []
        for stone in player.placed_stones:
            if stone.is_movable():
                queen_placed_moves += stone.return_moves(game)

        return queen_placed_moves

    def queen_not_placed():
        """
        Return all possible moves if queen has not been placed,
        pieces cannot move and queen has to be placedn if it
        is move 7 or 8
        """
        queen_not_placed_moves = []
        placing_positions = return_placing_positions()
        if game.turn == 7 or game.turn == 8:
            for stone in player.available_stones:
                if stone.kind == QUEEN:
                    queen_not_placed_moves += stone.return_placing_moves(placing_positions)
                    break
        else:
            for stone in player.available_stones:
                queen_not_placed_moves += stone.return_placing_moves(placing_positions)
        return queen_not_placed_moves

    if game.turn == 1 or game.turn == 2:
        available_moves = first_second_turn()
    elif player.queen:
        available_moves = queen_placed()
    else:
        available_moves = queen_not_placed()

    return available_moves


def make_connections(stone, game):
    """Creates all new connections for the stone according to positions around it"""
    for count in range(NUM_OF_CONNECTIONS):
        if check_position(game, stone.position, count) != PLACEHOLDER:
            set_new_connection(game, stone, count)


def make_move(game, move, current_player, other_player):
    """Make move

    :param game:
    :param move: move containing which stone is going to be moved and where
    :param current_player: Player making the move
    :param other_player: Player who is not making current move
    :return:
    """
    def place_stone(stone, position, player):
        stone.position = position
        player.placed_stones.append(stone)
        player.available_stones.remove(stone)
        game.placed_stones.append(stone)
        game.board[position[0]][position[1]] = stone
        if stone.kind == QUEEN:
            player.queen = stone

    def move_stone(stone, position):
        """Move stone to position

        :param stone: stone which is to be moved
        :param position: position where the stone is going to be moved
        """
        def move_beetle():
            """Make move with beetle"""
            def free_stone_under():
                """Makes stone which was under beetle movable again"""
                if stone == current_player.queen:
                    current_player.queen = stone.under
                elif stone == other_player.queen:
                    other_player.queen = stone.under

                game.board[stone.position[0]][stone.position[1]] = stone.under

                stone.under.above = False

                make_connections(stone.under, game)

            def add_stone_under():
                """Adds stone under beetle"""
                if game.board[position[0]][position[1]] != PLACEHOLDER:
                    stone.under = game.board[position[0]][position[1]]
                    clean_connections(stone.under)
                    stone.under.above = stone
                    if stone.under == current_player.queen:
                        current_player.queen = stone
                    elif stone.under == current_player.queen:
                        current_player.queen = stone

            if stone.under:
                free_stone_under()
                stone.under = None
                stone.connections = [PLACEHOLDER] * NUM_OF_CONNECTIONS
            else:
                game.board[stone.position[0]][stone.position[1]] = PLACEHOLDER
                clean_connections(stone)

            add_stone_under()

        if stone.kind == BEETLE:
            move_beetle()
        else:
            game.board[stone.position[0]][stone.position[1]] = PLACEHOLDER
            clean_connections(stone)
        stone.position = position
        game.board[position[0]][position[1]] = stone
        make_connections(stone, game)

    def clean_connections(stone):
        """Sets all connections of stone to PLACEHOLDER"""
        for count in range(NUM_OF_CONNECTIONS):
            if stone.connections[count] != PLACEHOLDER:
                stone.connections[count].connections[(count + 3) % NUM_OF_CONNECTIONS] = PLACEHOLDER
                stone.connections[count] = PLACEHOLDER

    if move.stone in current_player.available_stones:
        place_stone(move.stone, move.position, current_player)
    else:
        move_stone(move.stone, move.position)

    make_connections(move.stone, game)


def choose_random_move(available_moves):
    """Choose random move from available_moves received"""
    number_of_moves = len(available_moves) - 1
    move = randint(0, number_of_moves)
    return move


def ai_turn():
    """Perform AI turn"""


def players_turn(game, current_player, opponent, available_moves):
    """Perform human player's turn"""
    print("")
    print(game)
    print(f"Player1 hand: {current_player.available_stones}")
    print(f"Player2 hand: {opponent.available_stones}")
    print("")
    for stone in game.placed_stones:
        if stone.kind == BEETLE:
            if stone.under:
                print(f"Under {stone} there is {stone.under}")
            else:
                print(f"There is nothing under {stone}")
    print("")
    print(f"Its turn: {game.turn}")

    print("")

    print(f"{current_player} chooses a move")

    print("")
    move_count = 0
    for move in available_moves:
        print(move_count, end=" ")
        print(move)
        move_count += 1

    while True:
        try:
            move = int(input("Choose move: "))
            make_move(game, available_moves[move], current_player, opponent)
        except (ValueError, IndexError):
            print("Enter correct move")
        else:
            break


def random_turn(game, current_player, opponent, available_moves):
    """Function making random move"""
    move_num = choose_random_move(available_moves)
    move = available_moves[move_num]
    make_move(game, move, current_player, opponent)
    print('Opponent moved {} to {}'.format(move.stone, move.position))


def main():
    """Function running the Hive game"""
    game = Game()
    player1 = Player("W")
    player2 = Player("B")
    opponents = [players_turn, random_turn]
    choices = '''If you want to play game of two players enter "0",
    if you want to play against random opponent enter "1",
    if you want to play against AI enter "2"
    '''

    while True:
        try:
            print(choices)
            choice = int(input("Choose opponent: "))
            if choice == 2:
                print("I'm sorry but AI opponent is currently not available")
                raise ValueError
            opponent = opponents[choice]
        except (ValueError, IndexError):
            print("Enter correct opponent")
        else:
            break

    while True:
        print('turn is', game.turn)
        if game.turn % 2 == 1:
            current_player = player1
            another_player = player2
            available_moves = find_available_moves(current_player, game)

            if not available_moves:
                print('no moves available for player 1')
            else:
                random_turn(game, current_player, another_player, available_moves)
        else:
            current_player = player2
            another_player = player1
            available_moves = find_available_moves(current_player, game)

            if not available_moves:
                print('no moves available for player 2')
            else:
                opponent(game, current_player, another_player, available_moves)

        if is_game_terminal(player1, player2):
            print(game)
            print(player1.queen.position)
            print(player1.queen.connections)
            print(player2.queen.position)
            print(player2.queen.connections)
            break
        game.turn += 1


if __name__ == "__main__":
    main()
