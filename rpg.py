from intro import player_name, player_class, player_level, mana, capacity, strength, dexterity, energy, experience
import random
from time import sleep
import os
import csv

levels_to_create = 3

def getch():
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def display_inventory(inventory, ch, order=None):
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


def create_board(width, height,level,door_pos_right=19,door_pos_left=5):
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
                    #if door_pos_left == middle_door or door_pos_right == middle_door:
                #        if door_pos_right == middle_door:
            #                board_row.append("→")
        #                    middle_door += 1
    #                    elif level > 1 and door_pos_left == middle_door:
    #                        board_row.append("←")
    #                        middle_door += 1
    #                    elif not door_pos_left == middle_door and not door_pos_left == middle_door:
    #                        board_row.append("X")
    #                        middle_door += 1 '''
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
                        if door_pos_right == middle_door and not levels_to_create-1 == level:
                            board_row.append("→")
                            middle_door += 1
                        elif levels_to_create-1 == level and door_pos_right == middle_door:
                            board_row.append("X")
                else:
                    board_row.append(".")
        board.append(board_row)

    for i in range(15):
        char = '🌵'
        x_generator = random.randrange(5,25)
        y_generator = random.randrange(5,75)
        board[x_generator][y_generator] = char
        board[x_generator-1][y_generator] = char
        board[x_generator+1][y_generator] = char
        board[x_generator][y_generator+1] = char
        board[x_generator][y_generator-1] = char
        board[x_generator-1][y_generator-1] = char
        board[x_generator+1][y_generator+1] = char
        board[x_generator+1][y_generator-1] = char
        board[x_generator-1][y_generator+1] = char

    mob_list = ['🦁','🐷','🦂','😆','😈','☪','✡','🎠','🌝','♞','😻']
    for i in range(8):
        x_generator = random.randrange(2,28)
        y_generator = random.randrange(2,78)
        random_mob = random.randrange(len(mob_list))
        insert_element(board, y_generator, x_generator, mob_list[random_mob])
        mob_list.pop(random_mob)


    #for i in range(1):
    #    x_generator = random.randrange(2,28)
    #    y_generator = random.randrange(2,78)
    #    insert_element(board, y_generator, x_generator, '🔪')


    with open('map{}.txt'.format(level), 'w') as out:
        out.write('\n'.join(str(''.join(row)) for row in board))
    return board


def import_map(filename, level):
    map_one = []
    with open('map{}.txt'.format(level), 'r', newline='') as board:
        for row in board:
            map_one.append(list(row.rstrip('\n')))
    return map_one


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


def generate_lands(width, height, count=5):
    y_generator = random.randrange(0, width)
    x_generator = random.randrange(0, height)

    with open('map.txt', 'a') as out:
        out.write(str(x_generator)+'\n'+str(y_generator)+'\n')


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


def health(hp):
    health = []
    for i in range(0, hp):
        health.append("♥")
    return health




def main():
    level = 0
#    board = create_board(80,30,level)
    x_player = 1
    y_player = 1
    life = 5
    inventory = {'gold coin': 3, 'torch': 4}
    for i in range(levels_to_create):
        create_board(80, 30,i,)
    while True:
        character = getch()
        force_exit(character)
        os.system('clear')
        board = import_map('map{}.txt'.format(level), level)
        if not board[y_player + y_movement(character)][x_player + x_movement(character)] == 'X':
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
            board = import_map('map{}.txt'.format(level), level)



        board_with_player = insert_player(board, x_player, y_player)
        print_board(board_with_player)
        display_inventory(inventory, character)
        print("Name: {0}, Class: {1}, Stage:{2}, Life:{3}, Mana:{4}, EXP:{5}, Str:{6}, Dex:{7}, Ene:{8}".format(
        player_name, player_class, level, str(''.join(health(life))), mana, experience, strength, dexterity, energy))


main()
