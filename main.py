pos_ar = [(-1, -1), (-1, 1), (0, 2), (1, 1), (1, -1), (0, -2)]


class Board:
    def __init__(self, turn=0, size=68):
        self.turn = turn
        self.size = size
        self.board = []
        for y in range(self.size):
            self.board.append([])
            for x in range(self.size):
                if x % 2 == y % 2:
                    self.board[y].append("0")
                else:
                    self.board[y].append("-")
        self.available_moves = []
        self.placed_stones = []

    def __str__(self):
        left = self.size
        right = 0
        top = 0
        bottom = self.size-1
        for y in range(self.size):
            for stone in self.placed_stones:
                if stone in self.board[y]:
                    top = y
                    break
            if top != 0:
                break
        for y in reversed(range(self.size)):
            for stone in self.placed_stones:
                if stone in self.board[y]:
                    bottom = y
                    break
            if bottom != self.size-1:
                break
        for y in range(top, bottom+1):
            for x in range(self.size):
                if self.board[y][x] != "-" and self.board[y][x] != "0":
                    if x < left:
                        left = x
                    if x > right:
                        right = x
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
                if self.board[y][x] == "0":
                    res += " 0 "
                elif self.board[y][x] == "-":
                    res += " - "
                else:

                    res += str(self.board[y][x])
        res += "\n"
        return res

    def check_moves(self, player):
        def placing_stones(player):
            placing_positions = []
            for stone in player.placed_stones:
                for c in range(6):
                    possible_move = [stone.position[0]+pos_ar[c][0], stone.position[1]+pos_ar[c][1]]
                    if possible_move not in placing_positions:
                        if self.board[possible_move[0]][possible_move[1]] == "0":
                            for c2 in range(6):
                                if self.board[possible_move[0]+pos_ar[c2][0]][possible_move[1]+pos_ar[c2][1]] == "0":
                                    pass
                                elif self.board[possible_move[0]+pos_ar[c2][0]][possible_move[1]+pos_ar[c2][1]].colour == player.colour:
                                    pass
                                else:
                                    break
                            else:
                                placing_positions.append(possible_move)
            return placing_positions

        def moving_stones(player):
            def check_if_movable(stone):
                if stone.kind == "B":
                    if stone.under:
                        return True
                for stone2 in self.placed_stones:
                    if stone2.kind == "B":
                        if stone2.under:
                            if stone2.under == stone:
                                return False
                free_positions = stone.connections.count("0")
                if free_positions == 0 or free_positions == 1 or free_positions == 5:
                    return True
                else:
                    for c in range (6):
                        if stone.connections[c] != "0":
                            if stone.connections[(c+1)%6] == "0" and stone.connections[(c-1)%6] == "0":
                                #check if board.placed_stones is more then minimal number to create circle
                                track_positions = [stone.connections[c]]
                                closed_positions = [stone]
                                for c2 in range(6):
                                    if c2 != (c+3)%6:
                                        #opposite to original stone

                                        if track_positions[0].connections[c2] != "0" and track_positions[0].connections[c2] not in closed_positions:
                                            track_positions.append(track_positions[0].connections[c2])
                                else:
                                    closed_positions.append(track_positions[0])
                                    del track_positions[0]

                                while track_positions != []:
                                    for c2 in range(6):
                                        if track_positions[0].connections[c2] == stone:
                                            return True
                                        elif track_positions[0].connections[c2] != "0" and track_positions[0].connections[c2] not in closed_positions:
                                            track_positions.append(track_positions[0].connections[c2])
                                    else:
                                        closed_positions.append(track_positions[0])
                                        del track_positions[0]
                                else:
                                    return False

                                #do for loop again and always check if positon does or doesnt eqal closed_positions[0]


                    else:
                        return True

            def check_surounded(stone):
                for c in range(6):
                    if stone.connections[c] == "0" and (stone.connections[(c-1) % 6] == "0" or stone.connections[(c+1) % 6] == "0"):
                        return False
                else:
                    return True

            def basic_move(stone, depth):

                possible_moves = [stone.position]
                available_positions = []
                closed_positions = []
                d = 0
                while possible_moves != []:
                    if d == depth:
                        return available_positions
                    count = 0
                    y = possible_moves[0][0]
                    x = possible_moves[0][1]
                    for i in range(6):
                        if self.board[y+pos_ar[i][0]][x+pos_ar[i][1]] != "0":
                            break
                    for c in range(i, i+7):
                        #need to start from possition which is not 0 as othervise it messes it up, because of that i
                        if self.board[y+pos_ar[c % 6][0]][x+pos_ar[c%6][1]] == "0":
                            count += 1
                        elif count > 1:
                            next_position = (y+pos_ar[(c-count) % 6][0], x+pos_ar[(c-count) % 6][1])
                            if next_position not in closed_positions:
                                possible_moves.append(next_position)
                                if (d == 2 or depth != 3) and next_position != stone.position and next_position not in available_positions:
                                    available_positions.append(next_position)
                            next_position = (y+pos_ar[(c-1)%6][0], x+pos_ar[(c-1) % 6][1])
                            if next_position not in closed_positions:
                                possible_moves.append(next_position)
                                if (d == 2 or depth != 3) and next_position != stone.position and next_position not in available_positions:
                                    available_positions.append(next_position)

                            if count == 2 and c < i+4:
                                count = 0
                            else:
                                break
                        else:
                            count = 0

                    closed_positions.append(possible_moves[0])
                    del possible_moves[0]

                    d += 1
                return available_positions

            def queen_moves(stone):
                if check_surounded(stone):
                    return
                else:
                    available_positions = basic_move(stone,1)

                    for position in available_positions:
                        self.available_moves.append(Avail_Position(stone,position))

            def spider_moves(stone):
                if check_surounded(stone):
                    return
                else:
                    available_positions = basic_move(stone, 3)

                    for position in available_positions:
                        self.available_moves.append(Avail_Position(stone, position))

            def grasshopper_moves(stone):
                for c in range(6):
                    if stone.connections[c] != "0":
                        possible_position = stone
                        while possible_position.connections[c] != "0":
                            possible_position = possible_position.connections[c]
                        else: self.available_moves.append(Avail_Position(stone, (possible_position.position[0]+pos_ar[c][0],possible_position.position[1]+pos_ar[c][1])))

            def beetle_moves(stone):
                if check_surounded(stone):
                    return
                else:
                    available_positions = basic_move(stone, 1)

                    for position in available_positions:
                        self.available_moves.append(Avail_Position(stone, position))


                for c in range(6):
                    if stone.connections[c] != "0":
                        position = (stone.position[0]+pos_ar[c][0], stone.position[1]+pos_ar[c][1])
                        self.available_moves.append(Avail_Position(stone,position))
                    elif stone.under:
                        position = (stone.position[0]+pos_ar[c][0], stone.position[1]+pos_ar[c][1])
                        avail_pos = Avail_Position(stone,position)
                        if avail_pos not in self.available_moves:
                            self.available_moves.append(avail_pos)

                    #add moves on top of other stone

            def ant_moves(stone):
                if check_surounded(stone):
                    return
                else:
                    available_positions = basic_move(stone, 100)

                    for position in available_positions:
                        self.available_moves.append(Avail_Position(stone, position))

            for stone in player.placed_stones:
                if check_if_movable(stone):
                    if stone.kind == "Q":
                        queen_moves(stone)
                    elif stone.kind == "S":
                        spider_moves(stone)

                    elif stone.kind == "G":
                        grasshopper_moves(stone)

                    elif stone.kind == "B":
                        beetle_moves(stone)

                    elif stone.kind == "A":
                        ant_moves(stone)

        self.available_moves = []
        if self.turn == 0:
            #any stone can be placed at [17][17]
            for stone in player.available_stones:
                if stone.kind not in ["Q"]:
                    self.available_moves.append(Avail_Position(stone, (34, 34)))
        elif self.turn == 1:
            for stone in player.available_stones:
                if stone.kind not in ["Q"]:
                    self.available_moves.append(Avail_Position(stone, (34, 36)))
        elif player.queen_placed:
            placing_positions = placing_stones(player)
            for position in placing_positions:
                for stone in player.available_stones:
                    self.available_moves.append(Avail_Position(stone, position))
            moving_stones(player)
        elif player.colour == "W":
            if self.turn == 6:
                placing_positions = placing_stones(player)
                for position in placing_positions:
                    self.available_moves.append(Avail_Position(white_queen, (position)))
                #queen can be placed for possible placing position on board where only the colour is touching

                #might need to define queen of each colour
            else:
                placing_positions = placing_stones(player)
                for position in placing_positions:
                    for stone in player.available_stones:
                        self.available_moves.append(Avail_Position(stone, position))

        elif player.colour == "B":
            if self.turn == 7:
                placing_positions = placing_stones(player)
                for position in placing_positions:
                    self.available_moves.append(Avail_Position(black_queen, position))

                # queen can be placed for possible placing position on board where only the colour is touching

                # might need to define queen of each colour

            else:
                placing_positions = placing_stones(player)
                for position in placing_positions:
                    for stone in player.available_stones:
                        self.available_moves.append(Avail_Position(stone, position))

    def move_stone(self, stone, position, player):
        #gonna be different for beetle moving
        if stone in player.available_stones:
            stone.position = position
            player.placed_stones.append(stone)
            player.available_stones.remove(stone)
            self.placed_stones.append(stone)
            self.board[position[0]][position[1]] = stone
            if stone.kind == "Q":
                player.queen_placed = True
        else:
            if stone.kind == "B":
                global black_queen
                global white_queen

                if stone.under:

                    if stone == black_queen:
                        black_queen = stone.under
                    elif stone == white_queen:
                        white_queen = stone.under

                    self.board[stone.position[0]][stone.position[1]] = stone.under

                    for c in range(6):
                        if stone.connections[c] != "0":
                            stone.connections[c].connections[(c + 3) % 6] = stone.under
                            stone.under.connections[c] = stone.connections[c]
                            stone.connections[c] = "0"


                    stone.under = None
                else:
                    self.board[stone.position[0]][stone.position[1]] = "0"
                    for c in range(6):
                        if stone.connections[c] != "0":
                            stone.connections[c].connections[(c + 3) % 6] = "0"
                            stone.connections[c] = "0"

                if self.board[position[0]][position[1]] != "0":
                    stone.under = self.board[position[0]][position[1]]
                    if stone.under == black_queen:
                        black_queen = stone
                    elif stone.under == white_queen:
                        white_queen = stone

                stone.position = position
                self.board[position[0]][position[1]] = stone



            else:
                self.board[stone.position[0]][stone.position[1]] = "0"
                stone.position = position
                self.board[position[0]][position[1]] = stone
                for c in range(6):
                    if stone.connections[c] != "0":
                        stone.connections[c].connections[(c+3) % 6] = "0"
                        stone.connections[c] = "0"
        #adds connections for stone and stones touching it
        for c in range(6):
            if self.board[stone.position[0]+pos_ar[c][0]][stone.position[1]+pos_ar[c][1]] != "0":
                self.board[stone.position[0] + pos_ar[c][0]][stone.position[1] + pos_ar[c][1]].connections[(c+3) % 6] = stone
                stone.connections[c] = self.board[stone.position[0]+pos_ar[c][0]][stone.position[1]+pos_ar[c][1]]


class Stone:
    def __init__(self, kind, colour, index):
        self.kind = kind
        self.index = index
        self.colour = colour
        self.connections = ["0"]*6
        self.position = None
        if self.kind == "B":
            self.under = None

    def __str__(self):
        if self.kind == "Q":
            return "Q " + self.colour
        else:
            return self.kind + str(self.index)+ self.colour

    def __repr__(self):
        return self.__str__()

    def add_connection(self, position, stone):
        self.connections[position] = stone
        if stone.kind == "Q":
            if 0 in self.connections:
                return True
            else:
                return False
        else:
            return False

    def reove_connection(self,position):
        self.connections[position] = "0"


class AvailableStones:
    def __init__(self, colour, choice_of_stones=("Q", "S", "G", "B", "A")):
        self.available = []
        for stone in choice_of_stones:
            if stone in ["S", "B"]:
                for c in range(2):
                    self.available.append(Stone(stone, colour, c))
            elif stone in ["G", "A"]:
                for c in range(3):
                    self.available.append(Stone(stone, colour, c))
            else:
                if colour == "W":
                    global white_queen
                    white_queen = Stone(stone,colour, 1)
                    self.available.append(white_queen)
                else:
                    global black_queen
                    black_queen = Stone(stone,colour, 1)
                    self.available.append(black_queen)


class Avail_Position:
    def __init__(self, stone, position):
        self.stone = stone
        self.position = position

    def __eq__(self, other):
        return self.stone == other.stone and self.position == other.position

    def __str__(self):
        return "stone " + str(self.stone) + " position " + str(self.position[0]) + " " + str(self.position[1])

    def __repr__(self):
        return self.__str__()


class Player:
    def __init__(self, colour):
        self.colour = colour
        self.queen_placed = False
        self.available_stones = AvailableStones(colour).available
        self.placed_stones = []

    def __str__(self):
        if self.colour == "B":
            return "Second player"
        else:
            return "First player"


if __name__ == "__main__":
    board = Board()
    player1 = Player("W")
    player2 = Player("B")

    while True:
        print("")
        print(board)
        print("Player1 hand:", end=" ")
        print(player1.available_stones)
        print("Player2 hand:", end=" ")
        print(player2.available_stones)
        print("")
        for stone in board.placed_stones:
            if stone.kind == "B":
                if stone.under:
                    print(f"Under {stone} there is {stone.under}")
                else:
                    print(f"There is nothing under {stone}")
        print("")

        if board.turn % 2 == 0:
            current_player = player1
        else:
            current_player = player2

        print(f"Its turn: {board.turn}")

        print("")

        print(f"{current_player} chooses a move")

        print("")
        board.check_moves(current_player)
        c = 0
        for move in board.available_moves:
            print(c,end=" ")
            print(move)
            c+=1
        #find and print available moves

        #take input to choose move
        #stone = input("Choose stone: ")
        #y = input("position y: ")
        #x = input("position x: ")
        while True:
            try:
                move = int(input("Choose move: "))
                board.move_stone(board.available_moves[move].stone, board.available_moves[move].position, current_player)
            except:
                print("Enter correct move")
            else:
               break
        #make move
        #board.move_stone(stone, (y, x), current_player)
        board.move_stone(board.available_moves[move].stone, board.available_moves[move].position, current_player)
            #


        #checks if queens have been surrounded

        if black_queen.connections.count("0") == 0:
            if white_queen.connections.count("0") == 0:
                print("its a tie")
                break
            else:
                print("black lost")
                break
        if white_queen.connections.count("0") == 0:
            print("white lost")
            break
        board.turn += 1
    print(board)