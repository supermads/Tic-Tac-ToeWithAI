from random import randrange


class GameTable:
    def __init__(self):
        self.table = [[' ' for _i in range(3)] for _j in range(3)]
        self.x_count = 0
        self.o_count = 0
        self.open_spaces = [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]

    def print_table(self):
        print('-' * 9)
        print('|', self.table[0][0], self.table[0][1], self.table[0][2], '|')
        print('|', self.table[1][0], self.table[1][1], self.table[1][2], '|')
        print('|', self.table[2][0], self.table[2][1], self.table[2][2], '|')
        print('-' * 9)

    def find_winner(self):
        winner = ''
        win_conditions = [[self.table[0][0], self.table[0][1], self.table[0][2]], [self.table[1][0], self.table[1][1], self.table[1][2]],
                        [self.table[2][0], self.table[2][1], self.table[2][2]], [self.table[0][0], self.table[1][1], self.table[2][2]],
                        [self.table[0][2], self.table[1][1], self.table[2][0]], [self.table[0][0], self.table[1][0], self.table[2][0]],
                        [self.table[0][1], self.table[1][1], self.table[2][1]], [self.table[0][2], self.table[1][2], self.table[2][2]]]
        for condition in win_conditions:
            if condition[0] != ' ' and condition[0] == condition[1] == condition[2]:
                winner = condition[0]
        if winner:
            print('{} wins'.format(winner))
            return winner
        else:
            return None

    def computer_move(self, char_choice):
        a, b = self.open_spaces.pop(randrange(len(self.open_spaces)))
        if char_choice == 'X':
            self.table[a][b] = 'X'
            self.x_count += 1
        else:
            self.table[a][b] = 'O'
            self.o_count += 1
        print('Making move level "easy"')
        self.print_table()

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
                    self.computer_move('X')
                elif player_1 == 'user':
                    self.user_move('X')
            else:
                if player_2 == 'easy':
                    self.computer_move('O')
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
