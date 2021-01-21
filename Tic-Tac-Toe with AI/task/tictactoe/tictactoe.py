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


class GameTable:
    def __init__(self):
        self.table = [[' ' for _i in range(3)] for _j in range(3)]
        self.x_count = 0
        self.o_count = 0
        self.open_spaces = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
        self.win_conditions = [WinCondition(Point(0, 0), Point(0, 1), Point(0, 2)), WinCondition(Point(1, 0), Point(1, 1), Point(1, 2)),
            WinCondition(Point(2, 0), Point(2, 1), Point(2, 2)), WinCondition(Point(0, 0), Point(1, 1), Point(2, 2)),
            WinCondition(Point(0, 2), Point(1, 1), Point(2, 0)), WinCondition(Point(0, 0), Point(1, 0), Point(2, 0)),
            WinCondition(Point(0, 1), Point(1, 1), Point(2, 1)), WinCondition(Point(0, 2), Point(1, 2), Point(2, 2))]

    def get_spaces_for_win_condition(self, condition):
        space1 = self.table[condition.p1.a][condition.p1.b]
        space2 = self.table[condition.p2.a][condition.p2.b]
        space3 = self.table[condition.p3.a][condition.p3.b]
        return [space1, space2, space3]

    def print_table(self):
        print('-' * 9)
        print('|', self.table[0][0], self.table[0][1], self.table[0][2], '|')
        print('|', self.table[1][0], self.table[1][1], self.table[1][2], '|')
        print('|', self.table[2][0], self.table[2][1], self.table[2][2], '|')
        print('-' * 9)

    def find_winner(self):
        winner = ''
        for condition in self.win_conditions:
            space1, space2, space3 = self.get_spaces_for_win_condition(condition)
            if space1 != ' ' and space1 == space2 == space3:
                winner = space1
                print('{} wins'.format(winner))
                return winner
        return None

    def easy_move(self, char_choice, level='easy'):
        a, b = self.open_spaces.pop(randrange(len(self.open_spaces)))
        if char_choice == 'X':
            self.table[a][b] = 'X'
            self.x_count += 1
        else:
            self.table[a][b] = 'O'
            self.o_count += 1
        print('Making move level "{}"'.format(level))
        self.print_table()

    def medium_move(self, char_choice):
        move_made = False
        for condition in self.win_conditions:
            if not move_made:
                space1, space2, space3 = self.get_spaces_for_win_condition(condition)
                # If a win can be made in one move (by player or opponent), make that move
                if space1 != ' ' and space1 == space2 and space3 == ' ':
                    self.table[condition.p3.a][condition.p3.b] = char_choice
                    move_made = True
                elif space1 != ' ' and space1 == space3 and space2 == ' ':
                    self.table[condition.p2.a][condition.p2.b] = char_choice
                    move_made = True
                elif space2 != ' ' and space2 == space3 and space1 == ' ':
                    self.table[condition.p1.a][condition.p1.b] = char_choice
                    move_made = True
        if move_made:
            print('Making move level "medium"')
            self.print_table()
            if char_choice == 'X':
                self.x_count += 1
            else:
                self.o_count += 1
        else:
            self.easy_move(char_choice, 'medium')

    def user_move(self, char_choice):
        coord = input("Enter the coordinates: ")
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
                    if char_choice == 'X':
                        self.table[a][b] = 'X'
                        self.x_count += 1
                    else:
                        self.table[a][b] = 'O'
                        self.o_count += 1
                    space_taken = [a, b]
                    self.open_spaces.pop(self.open_spaces.index(space_taken))
                    self.print_table()
            else:
                print('You should enter numbers!')
        else:
            print('You should enter numbers!')

    def play(self, player_1, player_2):
        winner = ''
        while self.x_count + self.o_count < 9 and not winner:
            if self.x_count == self.o_count:
                if player_1 == 'easy':
                    self.easy_move('X')
                elif player_1 == 'medium':
                    self.medium_move('X')
                elif player_1 == 'user':
                    self.user_move('X')
            else:
                if player_2 == 'easy':
                    self.easy_move('O')
                elif player_2 == 'medium':
                    self.medium_move('O')
                elif player_2 == 'user':
                    self.user_move('O')
            winner = self.find_winner()
        if not winner:
            print("Draw")


def main():
    command = input('Input command: ')
    while command != 'exit':
        # Ready to play when start, player_1, and player_2 received from user
        ready = False
        while not ready:
            if command == 'exit':
                return
            command = command.split()
            if len(command) < 3 or command[0] != 'start':
                print('Bad parameters!')
                command = input('Input command: ')
            else:
                player_1 = command[1]
                player_2 = command[2]
                ready = True
        table = GameTable()
        table.play(player_1, player_2)
        command = input('\nInput command: ')


main()
