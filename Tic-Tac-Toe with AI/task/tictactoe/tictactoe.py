from copy import deepcopy
from random import randrange


class Point:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class WinCondition:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3


class Move(Point):
    def __init__(self, a, b, score=None):
        super(Move, self).__init__(a, b)
        self.score = score

    def __str__(self):
        return "a: {} b: {}, score: {}".format(self.a, self.b, self.score)


class Player:
    def __init__(self, player_type=None, char_choice=None):
        self.player_type = player_type
        self.char_choice = char_choice
        self.moves_made = 0


class GameTable:
    def __init__(self, player_1=None, player_2=None, initial_board_state=None):
        if initial_board_state is None:
            self.table = [[' ' for _i in range(3)] for _j in range(3)]
        else:
            self.table = initial_board_state
        self.win_conditions = [WinCondition(Point(0, 0), Point(0, 1), Point(0, 2)), WinCondition(Point(1, 0), Point(1, 1), Point(1, 2)),
            WinCondition(Point(2, 0), Point(2, 1), Point(2, 2)), WinCondition(Point(0, 0), Point(1, 1), Point(2, 2)),
            WinCondition(Point(0, 2), Point(1, 1), Point(2, 0)), WinCondition(Point(0, 0), Point(1, 0), Point(2, 0)),
            WinCondition(Point(0, 1), Point(1, 1), Point(2, 1)), WinCondition(Point(0, 2), Point(1, 2), Point(2, 2))]
        self.player_1 = player_1
        self.player_2 = player_2

    def find_open_spaces(self, table):
        open_spaces = []
        for i in range(3):
            for j in range(3):
                if table[i][j] == ' ':
                    open_spaces.append([i, j])
        return open_spaces

    def get_spaces_for_win_condition(self, condition, table):
        space1 = table[condition.p1.a][condition.p1.b]
        space2 = table[condition.p2.a][condition.p2.b]
        space3 = table[condition.p3.a][condition.p3.b]
        return [space1, space2, space3]

    def print_table(self):
        print('-' * 9)
        print('|', self.table[0][0], self.table[0][1], self.table[0][2], '|')
        print('|', self.table[1][0], self.table[1][1], self.table[1][2], '|')
        print('|', self.table[2][0], self.table[2][1], self.table[2][2], '|')
        print('-' * 9)

    def find_winner(self, table):
        winner = ''
        for condition in self.win_conditions:
            space1, space2, space3 = self.get_spaces_for_win_condition(condition, table)
            if space1 != ' ' and space1 == space2 == space3:
                winner = space1
                return winner
        return winner

    def get_curr_player(self):
        if len(self.find_open_spaces(self.table)) % 2 == 1:
            return self.player_1
        else:
            return self.player_2

    def easy_move(self, player):
        open_spaces = self.find_open_spaces(self.table)
        a, b = open_spaces.pop(randrange(len(open_spaces)))
        self.table[a][b] = player.char_choice
        player.moves_made += 1
        print('Making move level "{}"'.format(player.player_type))
        self.print_table()

    def medium_move(self, player):
        move_made = False
        for condition in self.win_conditions:
            if not move_made:
                curr_char = player.char_choice
                if curr_char == 'X':
                    other_char = 'O'
                else:
                    other_char = 'X'
                space1, space2, space3 = self.get_spaces_for_win_condition(condition, self.table)
                # If a win can be made in one move (by player or opponent), make that move, prioritizing a win for the current player
                if curr_char == space1 == space2 and space3 == ' ':
                    self.table[condition.p3.a][condition.p3.b] = curr_char
                    move_made = True
                elif curr_char == space1 == space3 and space2 == ' ':
                    self.table[condition.p2.a][condition.p2.b] = curr_char
                    move_made = True
                elif curr_char == space2 == space3 and space1 == ' ':
                    self.table[condition.p1.a][condition.p1.b] = curr_char
                    move_made = True
                elif other_char == space1 == space2 and space3 == ' ':
                    self.table[condition.p3.a][condition.p3.b] = curr_char
                    move_made = True
                elif other_char == space1 == space3 and space2 == ' ':
                    self.table[condition.p2.a][condition.p2.b] = curr_char
                    move_made = True
                elif other_char == space2 == space3 and space1 == ' ':
                    self.table[condition.p1.a][condition.p1.b] = curr_char
                    move_made = True
        if move_made:
            print('Making move level "medium"')
            self.print_table()
            player.moves_made += 1
        else:
            self.easy_move(player)

    def minimax(self, temp_table, player):
        avail_spaces = self.find_open_spaces(temp_table)
        curr_player = self.get_curr_player()
        if curr_player == self.player_1:
            other_player = self.player_2
        else:
            other_player = self.player_1
        # base case: if the game is over, return 0 for a draw, 10 for a win, or -10 for a loss
        winner = self.find_winner(temp_table)
        if winner == 'X' or winner == 'O':
            if winner == curr_player.char_choice:
                return 10
            return -10
        elif len(avail_spaces) == 0:
            return 0
        moves = []
        for i in range(len(avail_spaces)):
            a, b = avail_spaces[i]
            move = Move(a, b)
            temp_table[a][b] = player.char_choice
            if player == curr_player:
                result = self.minimax(temp_table, other_player)
                if type(result) == int:
                    move.score = result
                else:
                    move.score = result.score
            else:
                result = self.minimax(temp_table, curr_player)
                if type(result) == int:
                    move.score = result
                else:
                    move.score = result.score
            temp_table[a][b] = ' '
            moves.append(move)
        best_move = 0
        if player == curr_player:
            best_score = -1000
            for i in range(len(moves)):
                if moves[i].score > best_score:
                    best_move = i
                    best_score = moves[i].score
        else:
            best_score = 1000
            for i in range(len(moves)):
                if moves[i].score < best_score:
                    best_move = i
                    best_score = moves[i].score
        return moves[best_move]

    def hard_move(self, player):
        temp_table = deepcopy(self.table)
        move = self.minimax(temp_table, player)
        self.table[move.a][move.b] = player.char_choice
        player.moves_made += 1
        print('Making move level "hard"')
        self.print_table()

    def user_move(self, player):
        coord = input('Enter the coordinates: ')
        if len(coord.split()) == 2:
            a, b = coord.split()
            if a.isnumeric() and b.isnumeric():
                # Indexes are 0-2, coordinates are 1-3
                a = int(a) - 1
                b = int(b) - 1
                if not (0 <= a <= 2 and 0 <= b <= 2):
                    print('Coordinates should be from 1 to 3!')
                elif self.table[a][b] != ' ':
                    print('This cell is occupied! Choose another one!')
                else:
                    self.table[a][b] = player.char_choice
                    player.moves_made += 1
                    self.print_table()
            else:
                print('You should enter numbers!')
        else:
            print('You should enter numbers!')

    def play(self):
        winner = ''
        while self.player_1.moves_made + self.player_2.moves_made < 9 and not winner:
            if self.player_1.moves_made == self.player_2.moves_made:
                current_player = self.player_1
            else:
                current_player = self.player_2
            if current_player.player_type == 'easy':
                self.easy_move(current_player)
            elif current_player.player_type == 'medium':
                self.medium_move(current_player)
            elif current_player.player_type == 'hard':
                self.hard_move(current_player)
            elif current_player.player_type == 'user':
                self.user_move(current_player)
            winner = self.find_winner(self.table)
        if not winner:
            print("Draw")
        else:
            print('{} wins'.format(winner))


def main():
    player_options = ['user', 'easy', 'medium', 'hard']
    command = input('Input command: ')
    while command != 'exit':
        # Ready to play when start, player_1, and player_2 received from user
        ready = False
        while not ready:
            if command == 'exit':
                return
            command = command.split()
            if len(command) < 3 or command[0] != 'start' or command[1] not in player_options or command[2] not in player_options:
                print('Bad parameters!')
                command = input('Input command: ')
            else:
                player_1 = Player(command[1], 'X')
                player_2 = Player(command[2], 'O')
                ready = True
        table = GameTable(player_1, player_2)
        table.play()
        command = input('\nInput command: ')


main()
