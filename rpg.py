from intro import player_name, player_class
import random
from time import time
import os
import csv

levels_to_create = 3


def getch():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def create_board(width, height, level, door_pos_right=19, door_pos_left=5):
    board = []
    line = 0
    #  For door position:
    #  odd for arrow on right side,
    middle_door = 0  # even for arrow on left side
    for row in range(0, height):
        board_row = []
        for column in range(0, width):
            if row == 0 or row == height-1:
                board_row.append("X")
            else:  # if column == 0 or column == width - 1:
                if column == 0 or column == width - 1:
                    middle_door += 1
                    if not door_pos_right == middle_door and not door_pos_left == middle_door:
                        board_row.append("X")
                        middle_door += 1
                    else:
                        if level == 0 and door_pos_left == middle_door:
                            board_row.append("X")
                            middle_door += 1
                        elif door_pos_left == middle_door:
                            board_row.append("←")
                            middle_door += 1
                        if door_pos_right == middle_door and not levels_to_create - 1 == level:
                            board_row.append("→")
                            middle_door += 1
                        elif levels_to_create-1 == level and door_pos_right == middle_door:
                            board_row.append("X")
                else:
                    board_row.append(".")
        board.append(board_row)

    for i in range(15):
        char = '🏢'
        x_generator = random.randrange(5, 25)
        y_generator = random.randrange(5, 75)
        board[x_generator][y_generator] = char
        board[x_generator-1][y_generator] = char
        board[x_generator+1][y_generator] = char
        board[x_generator][y_generator+1] = char
        board[x_generator][y_generator-1] = char
        board[x_generator-1][y_generator-1] = char
        board[x_generator+1][y_generator+1] = char
        board[x_generator+1][y_generator-1] = char
        board[x_generator-1][y_generator+1] = char

    mob_list = ['😠','🐷','🤐','😆','😈','😈','😸','🤓','🌝','😱','😻']
    for i in range(8):
        x_generator = random.randrange(2,28)
        y_generator = random.randrange(2,78)
        random_mob = random.randrange(len(mob_list))
        insert_element(board, y_generator, x_generator, mob_list[random_mob])
        mob_list.pop(random_mob)

    with open('map{}.txt'.format(level), 'w') as out:
        out.write('\n'.join(str(''.join(row)) for row in board))

    return board


def import_map(filename, level):
    map_one = []
    with open('map{}.txt'.format(level), 'r', newline='') as board:
        for row in board:
            map_one.append(list(row.rstrip('\n')))
    return map_one


def import_stats(filename):
    stats_dict = {}
    with open(filename, 'r') as stats:
        reader = csv.reader(stats, delimiter=',')
        for row in reader:
            stats_dict[row[0]] = int(row[1])

    return stats_dict


def export_stats(dictionary, filename):
    with open('stats.csv', 'w') as stats:
        writer = csv.writer(stats, delimiter=',')
        writer.writerow(['player_level', dictionary['player_level']])
        writer.writerow(['life', dictionary['life']])
        writer.writerow(['capacity', dictionary['capacity']])
        writer.writerow(['strength', dictionary['strength']])
        writer.writerow(['dexterity', dictionary['dexterity']])
        writer.writerow(['energy', dictionary['energy']])
        writer.writerow(['experience', dictionary['experience']])
    stats.close()


def print_board(board):
    for row in board:
        for char in row:
            print(char, end='')
        print()


def insert_player(board, width, height):
    board[height][width] = "@"
    return board


def insert_element(board, width, height, symbol):
    board[height][width] = symbol
    return board


def x_movement(ch):
    if ch == 'a':
        return -1
    elif ch == 'd':
        return 1
    else:
        return 0


def y_movement(ch):
    if ch == 'w':
        return -1
    elif ch == 's':
        return 1
    else:
        return 0


def force_exit(ch):  # tymczasowy exit do fazy testów
    if ch == 'q':
        exit()


def display_inventory(inventory, ch, order='count,desc'):
    if ch == 'i':
        longest_string_count = 0
        for item in inventory:
            if len(item) > longest_string_count:
                longest_string_count = len(item)
        total_items = 0
        for item in inventory:
            total_items += inventory[item]
        print('Inventory:')
        print('{:>7}{:{align}{width}}'.format('count', 'item name', align='>', width=longest_string_count + 4))
        print('-' * (6 + len('count') + longest_string_count))
        if order == 'count,asc':
            sorted_inventory = [(key, inventory[key]) for key in sorted(inventory, key=inventory.get)]
            for key, value in sorted_inventory:
                print('{:>7}{:{align}{width}}'.format(value, key, align='>', width=longest_string_count + 4))
        elif order == 'count,desc':
            sorted_inventory = [(key, inventory[key]) for key in sorted(inventory, key=inventory.get, reverse=True)]
            for key, value in sorted_inventory:
                print('{:>7}{:{align}{width}}'.format(value, key, align='>', width=longest_string_count + 4))
        else:
            for item in inventory:
                print('{:>7}{:{align}{width}}'.format(inventory[item], item, align='>', width=longest_string_count + 4))
        print('-' * (6 + len('count') + longest_string_count))
        print("Total number of items: {}".format(total_items))


def add_to_inventory(inventory, added_items):
    for item in added_items:
        if item in inventory:
            inventory[item] += 1
        else:
            inventory[item] = 1
    return inventory


def attack(board, ch, level, stats, x_player, y_player):
    if ch == 'j':
        try:
            for i in range(1, stats['strength'] + 1):
                if not board[y_player][x_player + i] in ['😠','🐷','🤐','😆','😈','😈','😸','🤓','🌝','😱','😻']:
                    board[y_player][x_player + i] = '-'
                else:
                    board[y_player][x_player + i] = '.'
                    with open('map{}.txt'.format(level), 'w') as out:
                        out.write('\n'.join(str(''.join(row)) for row in board))
                    out.close()
                    stats['experience'] += 1
                    export_stats(stats, 'stats.csv')


        except IndexError:
            print("Out of range")
    if ch == 'k':
        try:
            for i in range(1, stats['dexterity'] + 1):
                if board[y_player][x_player + i] in ['😠','🐷','🤐','😆','😈','😈','😸','🤓','🌝','😱','😻']:
                    board[y_player][x_player + i] = 'x'
                    with open('map{}.txt'.format(level), 'w') as out:
                        out.write('\n'.join(str(''.join(row)) for row in board))
                    out.close()
                    stats['experience'] += 1
                    export_stats(stats, 'stats.csv')
        except IndexError:
            print("Out of range")

    if ch == 'l':
        if stats['energy'] > 0:
            board[y_player + 1][x_player + 1] = '*'
            board[y_player][x_player + 1] = '*'
            board[y_player - 1][x_player + 1] = '*'
            board[y_player + 1][x_player] = '*'
            board[y_player - 1][x_player] = '*'
            board[y_player - 1][x_player - 1] = '*'
            board[y_player][x_player - 1] = '*'
            board[y_player + 1][x_player - 1] = '*'

    return board


def health(hp):
    health = []
    for i in range(0, hp):
        health.append("♥")
    return health


def mob_movement(board, x_player, y_player, x_mob, y_mob, level):
    insert_player(board, x_player, y_player)
    if x_player < x_mob:
        x_mob -= 1
        if y_mob > y_player:
            y_mob -= 1
    else:
        x_mob += 1
        if y_mob < y_player:
            y_mob += 1

    if y_mob > y_player:
        y_mob -= 1

    if y_mob > y_player and x_mob > x_player:
        y_mob -= 1
        x_mob -= 1

    board = insert_element(board, x_mob, y_mob, '😆')
    import_map('map{}.txt'.format(level), level)
    return board

def main():
    level = 0
    board = create_board(80, 30, level)
    x_player = 1
    y_player = 1
    y_mob = random.randrange(2,28)
    x_mob = random.randrange(2,78)
    inventory = {'gold coin': 10, 'torch': 4}
    for i in range(levels_to_create):
        create_board(80, 30, i)


    while True:
        character = getch()
        force_exit(character)
        stats = import_stats('stats.csv')
        print(stats)
        board = insert_element(board, x_player, y_player, '.')
        with open('map{}.txt'.format(level), 'w') as out:
            out.write('\n'.join(str(''.join(row)) for row in board))
        board = import_map('map{}.txt'.format(level), level)
        if not board[y_player + y_movement(character)][x_player + x_movement(character)] in ['X','🏢','😠','🐷','🤐','😆','😈','😈','😸','🤓','🌝','😱','😻']:
            x_player = x_player + x_movement(character)
            y_player = y_player + y_movement(character)
        if board[y_player][x_player] == '→':
            x_player = 1
            y_player = 2
            level += 1
            board = import_map('map{}.txt'.format(level),level)
        if board[y_player][x_player] == '←':
            x_player = 78
            y_player = 5
            level -= 1


        board_with_player = insert_player(board, x_player, y_player)
        #board_with_player = mob_movement(board,x_player,y_player,x_mob,y_mob,level)
        print_board(board_with_player)
        os.system('clear')
        print_board(attack(board, character, level, stats, x_player, y_player))
        display_inventory(inventory, character)
        print("Name: {0}, Class: {1}, Level:{2}, Life:{3}, Stage: {4}, EXP: {5}, Str:{6}, Dex:{7}".format(
        player_name, player_class, stats['player_level'], stats['life'], level, stats['experience'], stats['strength'], stats['dexterity']))

if __name__ == '__main__':
    main()
