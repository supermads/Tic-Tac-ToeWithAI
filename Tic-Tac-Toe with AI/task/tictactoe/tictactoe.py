from random import randrange


def create_table():
    return [[' ' for _i in range(3)] for _j in range(3)]


def print_table(table):
    print('-' * 9)
    print('|', table[0][0], table[0][1], table[0][2], '|')
    print('|', table[1][0], table[1][1], table[1][2], '|')
    print('|', table[2][0], table[2][1], table[2][2], '|')
    print('-' * 9)


def find_winner(table):
    winner = ''
    win_conditions = [[table[0][0], table[0][1], table[0][2]], [table[1][0], table[1][1], table[1][2]],
                      [table[2][0], table[2][1], table[2][2]], [table[0][0], table[1][1], table[2][2]],
                      [table[0][2], table[1][1], table[2][0]], [table[0][0], table[1][0], table[2][0]],
                      [table[0][1], table[1][1], table[2][1]], [table[0][2], table[1][2], table[2][2]]]
    for condition in win_conditions:
        if condition[0] != ' ' and condition[0] == condition[1] == condition[2]:
            winner = condition[0]
    if winner:
        print('{} wins'.format(winner))
        return winner
    else:
        return None


def main():
    table = create_table()
    open_spaces = [table[0][0], table[0][1], table[0][2], table[1][0], table[1][1], table[1][2], table[2][0], table[2][1], table[2][2]]
    x_count = 0
    o_count = 0
    print_table(table)
    winner = ''
    while x_count + o_count < 9 and not winner:
        if x_count == o_count:
            coord = input("Enter the coordinates: ")
            if len(coord.split()) == 2:
                a, b = coord.split()
                if a.isnumeric() and b.isnumeric():
                    # Indexes are 0-2, coordinates are 1-3
                    a = int(a) - 1
                    b = int(b) - 1
                    if not (0 <= a <= 2 and 0 <= b <= 2):
                        print('Coordinates should be from 1 to 3!')
                    elif table[a][b] != ' ':
                        print('This cell is occupied! Choose another one!')
                    else:
                        table[a][b] = 'X'
                        x_count += 1
                        for space in open_spaces:
                            if space != ' ':
                                open_spaces.pop(open_spaces.index(space))
                        print_table(table)
                else:
                    print('You should enter numbers!')
            else:
                print('You should enter numbers!')
        else:
            # Assign a random open space to O
            open_spaces[randrange(len(open_spaces))] = 'O'
            o_count += 1
            print('Making move level "easy"')
            print_table(table)
        winner = find_winner(table)
    if not winner:
        print("Draw")


main()
