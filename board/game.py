from board.globals import FREE_SPACE, PLACEHOLDER


class Game:
    def __init__(self, turn=1, size=68, board = None, placed_stones=[]):
        self.turn = turn
        self.size = size
        if board:
            self.board = board
        else:
            self.board = create_board(size)
        self.placed_stones = placed_stones

    def __str__(self):
        def find_first_stone_from_top():
            for y in range(self.size):
                for item in self.board[y]:
                    if item is not PLACEHOLDER or item is not FREE_SPACE:
                        return y
            return 0

        def find_first_stone_from_bottom():
            for y in reversed(range(self.size)):
                for item in self.board[y]:
                    if item is not PLACEHOLDER or item is not FREE_SPACE:
                        return y
            return self.size - 1

        def find_first_left_right(top, bottom):
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

        left, right = find_first_left_right(top, bottom)

        if left == self.size and right == 0:
            res = "No stones have been placed so far"
        else:
            res = "   "
            for x in range(left, right+1):
                res += str(x)
                if x < 10:
                    res += "  "
                else:
                    res += " "
            for y in range(top, bottom+1):
                res += "\n"
                res += str(y)
                res += " "
                for x in range(left, right+1):
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


def create_board(size):
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
    if player.queen:
        return player.queen.connections.count(FREE_SPACE) == 0


def is_game_terminal(player1, player2):
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


if __name__ == "__main__":
    game = Game()
    game.board[0][0] = "A"
    game.board[1][1] = "Q"
    game.board[10][10] = "B"

    print(game)
    board = create_board(64)

    board[0][0] = "A"
    board[60][60] = "B"

    print(board)

    board[2][1] = FREE_SPACE

    game2 = Game(board=board, size=4)

    print(game2)

    print(game2.board)
