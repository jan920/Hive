from board.globals import FREE_SPACE, PLACEHOLDER, set_new_connection, check_position, NUM_OF_CONNECTIONS, BEETLE, \
                            QUEEN, GRASSHOPPER, ANT, SPIDER, count_new_position

from board.player import Player

from board.stones import AvailMove

class Game:
    """Class representing game of Hive"""
    def __init__(self, turn=1, size=68, board = None, placed_stones=[]):
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
            for y in range(self.size):
                for item in self.board[y]:
                    if item is not PLACEHOLDER and item is not FREE_SPACE:
                        return y
            return 0

        def find_first_stone_from_bottom():
            """Find last line which contains stone"""
            for y in reversed(range(self.size)):
                for item in self.board[y]:
                    if item is not PLACEHOLDER and item is not FREE_SPACE:
                        return y
            return self.size - 1

        def find_first_left_right():
            """"Find left, right most position of stone, withing area limited by top, bottom arguments received"""
            left = self.size
            right = 0
            for y in range(top, bottom + 1):
                for counter, item in enumerate(self.board[y]):
                    if item is not PLACEHOLDER and item is not FREE_SPACE:
                        if counter < left:
                            left = counter
                        if counter > right:
                            right = counter
            return left, right

        top = find_first_stone_from_top()

        bottom = find_first_stone_from_bottom()

        left, right = find_first_left_right()

        if left == self.size and right == 0:
            res = "No stones have been placed so far"
        else:
            res = "   "
            for x in range(left-2, right+3):
                res += str(x)
                if x < 10:
                    res += "  "
                else:
                    res += " "
            for y in range(top-1, bottom+2):
                res += "\n"
                res += str(y)
                res += " "
                for x in range(left-2, right+3):
                    if self.board[y][x] == FREE_SPACE:
                        res += " 0 "
                    elif self.board[y][x] == PLACEHOLDER:
                        res += " - "
                    else:
                        res += str(self.board[y][x])
            res += "\n"

        return res

    def __repr__(self):
        return self.__str__()


def is_terminal(player1, player2):
    if player1.queen:
        if player1.queen.connections.count(FREE_SPACE) == 0:
            if player2.queen.connections.count(FREE_SPACE) == 0:
                print("its a tie")
                return True
            else:
                print("white lost")
                return True
    if player2.queen:
        if player2.queen.connections.count(FREE_SPACE) == 0:
            print("black lost")
            return True


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
    for y in range(size):
        board.append([])
        for x in range(size):
            if x % 2 == y % 2:
                board[y].append(FREE_SPACE)
            else:
                board[y].append(PLACEHOLDER)
    return board


def is_players_queen_surrounded(player):
    """Return boolean if queen is surrounded"""
    if player.queen:
        return player.queen.connections.count(FREE_SPACE) == 0


def is_game_terminal(player1, player2):
    """Return boolean if game is terminal"""
    if is_players_queen_surrounded(player1):
        if is_players_queen_surrounded(player2):
            print("its a tie")
            return True
        else:
            print("player 2 lost")
            return True
    elif is_players_queen_surrounded(player2):
        print("player 1 lost")
        return True
    else:
        return False


def create_game(size=64, stones=[]):
    """Create game from received stones

    :param size: positive integer stating size of the board for the game
    :param stones: list of stones
    :return: created game
    :raise
    ValueError: if size not integer
    ValueError: if stones are not stone class, miss property position
    ValueError: if stones position is not correct

    """

    board = Game(turn=1, size=size, board = None, placed_stones=[stones])

    for stone in stones:
        if stone.position[0] % 2 == stone.position[1] % 2:
            board[stone.position[0]][stone.position[1]] = stone


        else:
            raise ValueError('stone stone position ')


def find_available_moves(player, game):
    def return_placing_positions():
        def check_placable(move):
            if game.board[move[0]][move[1]] == FREE_SPACE:
                for c in range(NUM_OF_CONNECTIONS):
                    condition1 = check_position(game, move, c) == FREE_SPACE
                    condition2 = check_position(game, move, c) in player.placed_stones
                    if not (condition1 or condition2):
                        return []
                else:
                    return move
            else:
                return []

        placing_positions = []
        for stone in player.placed_stones:
            for c in range(NUM_OF_CONNECTIONS):
                possible_position = count_new_position(stone.position, c)
                if possible_position not in placing_positions:
                    if check_placable(possible_position):
                        placing_positions.append(possible_position)
        return placing_positions

    def return_placing_moves():
        placing_moves = []
        placing_positions = return_placing_positions()
        for stone in player.available_stones:
            placing_moves += stone.return_placing_moves(placing_positions)
        return placing_moves

    def first_second_turn():
        available_moves = []
        if game.turn == 1:
            position = (34, 34)
        else:
            position = (34, 36)
        for stone in player.available_stones:
            if stone.kind not in [QUEEN]:
                available_moves.append(AvailMove(stone, position))
        return available_moves

    def queen_placed():
        available_moves = return_placing_moves()
        for stone in player.placed_stones:
            if stone.is_movable():
                available_moves += stone.return_moves(game)
        return available_moves

    def queen_not_placed():
        available_moves = []
        placing_positions = return_placing_positions()
        if game.turn == 7 or game.turn == 8:
            for stone in player.available_stones:
                if stone.kind == QUEEN:
                    available_moves += stone.return_placing_moves(placing_positions)
        else:
            for stone in player.available_stones:
                available_moves += stone.return_placing_moves(placing_positions)
        return available_moves

    if game.turn == 1 or game.turn == 2:
        available_moves = first_second_turn()
    elif player.queen:
        available_moves = queen_placed()
    else:
        available_moves = queen_not_placed()

    return available_moves


def make_move(game, move, player1, player2):
    def place_stone(stone, position, player):
        stone.position = position
        player.placed_stones.append(stone)
        player.available_stones.remove(stone)
        game.placed_stones.append(stone)
        game.board[position[0]][position[1]] = stone
        if stone.kind == QUEEN:
            player.queen = stone

    def move_stone(stone, position):
        def move_beetle():
            def free_stone_under():
                if stone == player1.queen:
                    player1.queen = stone.under
                elif stone == player2.queen:
                    player2.queen = stone.under

                game.board[stone.position[0]][stone.position[1]] = stone.under

                make_connections(stone.under)

            def add_stone_under():
                if game.board[position[0]][position[1]] != FREE_SPACE:
                    stone.under = game.board[position[0]][position[1]]
                    if stone.under == player1.queen:
                        player1.queen = stone
                    elif stone.under == player1.queen:
                        player1.queen = stone

            if stone.under:
                free_stone_under()
                stone.under = None
                stone.connections = [FREE_SPACE] * NUM_OF_CONNECTIONS
            else:
                game.board[stone.position[0]][stone.position[1]] = FREE_SPACE
                clean_connections(stone)

            add_stone_under()

        if stone.kind == BEETLE:
            move_beetle()
        else:
            game.board[stone.position[0]][stone.position[1]] = FREE_SPACE
            clean_connections(stone)
        stone.position = position
        game.board[position[0]][position[1]] = stone
        make_connections(stone)

    def clean_connections(stone):
        """Sets all connections of stone to FREE_SPACE placeholder"""
        for c in range(NUM_OF_CONNECTIONS):
            if stone.connections[c] != FREE_SPACE:
                stone.connections[c].connections[(c + 3) % NUM_OF_CONNECTIONS] = FREE_SPACE
                stone.connections[c] = FREE_SPACE

    def make_connections(stone):
        for c in range(NUM_OF_CONNECTIONS):
            if check_position(game, stone.position, c) != FREE_SPACE:
                set_new_connection(game, stone, c)

    if move.stone in player1.available_stones:
        place_stone(move.stone, move.position, player1)
    else:
        move_stone(move.stone, move.position)

    make_connections(move.stone)
    game.turn += 1


def main():
    game = Game()
    player1 = Player("W")
    player2 = Player("B")

    while True:
        print("")
        print(game)
        print("Player1 hand:", end=" ")
        print(player1.available_stones)
        print("Player2 hand:", end=" ")
        print(player2.available_stones)
        print("")
        for stone in game.placed_stones:
            if stone.kind == BEETLE:
                if stone.under:
                    print(f"Under {stone} there is {stone.under}")
                else:
                    print(f"There is nothing under {stone}")
        print("")

        if game.turn % 2 == 1:
            current_player = player1
            another_player = player2
        else:
            current_player = player2
            another_player = player1
        print(f"Its turn: {game.turn}")

        print("")

        print(f"{current_player} chooses a move")

        print("")
        available_moves = find_available_moves(current_player, game)
        c = 0
        for move in available_moves:
            print(c, end=" ")
            print(move)
            c += 1

        while True:
            try:
                move = int(input("Choose move: "))
                make_move(game, available_moves[move], current_player, another_player)
            except:
                print("Enter correct move")
            else:
                break
        if is_terminal(player1, player2):
            print(game.board)
            break


if __name__ == "__main__":
    main()
