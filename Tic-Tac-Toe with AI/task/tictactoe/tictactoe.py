def create_table():
    inputs = input('Enter the cells: ')
    return [[inputs[i].replace('_', ' ') for i in range(3)],
             [inputs[j].replace('_', ' ') for j in range(3, 6)],
             [inputs[k].replace('_', ' ') for k in range(6, 9)]]


def print_table(table):
    print('-' * 9)
    print('|', table[0][0], table[0][1], table[0][2], '|')
    print('|', table[1][0], table[1][1], table[1][2], '|')
    print('|', table[2][0], table[2][1], table[2][2], '|')
    print('-' * 9)


def find_winner(table, x_count, o_count):
    winner = ''
    win_conditions = [[table[0][0], table[0][1], table[0][2]], [table[1][0], table[1][1], table[1][2]],
                      [table[2][0], table[2][1], table[2][2]], [table[0][0], table[1][1], table[2][2]],
                      [table[0][2], table[1][1], table[2][0]], [table[0][0], table[1][0], table[2][0]],
                      [table[0][1], table[1][1], table[2][1]], [table[0][2], table[1][2], table[2][2]]]
    for condition in win_conditions:
        if condition[0] == condition[1] == condition[2] and condition[0] != ' ':
            winner = condition[0]
    if winner:
        print('{} wins'.format(winner))
    elif x_count + o_count < 9:
        print('Game not finished')
    else:
        print('Draw')


def main():
    keep_playing = True
    table = create_table()
    x_count = 0
    o_count = 0
    for row in table:
        x_count += row.count('X')
        o_count += row.count('O')
    print_table(table)
    while keep_playing:
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
                    if x_count == o_count:
                        table[a][b] = 'X'
                        x_count += 1
                    else:
                        table[a][b] = 'O'
                        o_count += 1
                    print_table(table)
                    keep_playing = False
            else:
                print('You should enter numbers!')
        else:
            print('You should enter numbers!')
    find_winner(table, x_count, o_count)


main()


