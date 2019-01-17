from board.globals import FREE_SPACE, PLACEHOLDER


class Game:
    def __init__(self, turn=1, size=68, board=None, placed_stones=[]):
        self.turn = turn
        self.size = size
        if board:
            self.board = board
        else:
            self.board = create_board(size)
        self.placed_stones = placed_stones

    def __str__(self):
        def find_first_stone_from_top(self):
            top = 0
            for y in range(self.size):
                for x in self.board[y]:
                    if x is not PLACEHOLDER or x is not FREE_SPACE:
                        top = y
                        break
                if top != 0:
                    break
            return top

        def find_first_bottom(self):
            bottom = self.size-1
            for y in reversed(range(self.size)):
                for stone in self.placed_stones:
                    if stone in self.board[y]:
                        bottom = y
                        break
                if bottom != self.size - 1:
                    break
            return bottom

        def find_first_left_right(self, top, bottom):
            left = self.size
            right = 0
            for y in range(top, bottom + 1):
                for x in range(self.size):
                    if self.board[y][x] != PLACEHOLDER and self.board[y][x] != FREE_SPACE:
                        if x < left:
                            left = x
                        if x > right:
                            right = x
            return left, right

        top = find_first_top(self)

        bottom = find_first_bottom(self)

        left, right = find_first_left_right(self, top, bottom)

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

    def is_terminal(self, player1, player2):
        if player1.queen:
            if player1.queen.connections.count(FREE_SPACE) == 0:
                if player2.queen.connections.count(FREE_SPACE) == 0:
                    print("its a tie")
                    return True
                else:
                    print("black lost")
                    return True
        if player2.queen:
            if player2.queen.connections.count(FREE_SPACE) == 0:
                print("white lost")
                return True


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
