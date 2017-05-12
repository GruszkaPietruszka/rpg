from intro import player_name, player_class, levels_to_create, start_timer
from hotwarm import hot_warm  # imports the hot-warm-cold game
import random
from time import time, sleep
import os
import csv


def getch():
    '''Functions returns the key pressed without having to input it with ENTER'''
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
    '''Returns a random-generated board with random-generated mobs and items

        Args:
            width: amount of characters printed in one line (the width of the board)
            height: amount of lines of characters printed (the height of the board)
            level: the exact level for which the board is generated
            (in game it is closed in a for loop which repeats the function for as many times,
            as is given in the levels_to_create variable from intro.py)
            door_pos_right: the index of the position of right-hand side exit on the board
            door_pos_left: the index of the position of left-hand side exit on the board
            '''
    board = []
    line = 0
    #  For door position:
    #  odd for arrow on right side,
    middle_door = 0  # even for arrow on left side O CO CHODZI Z MIDDLE DOOR?
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

    for i in range(15):  # generates as much 3x3 blocks of obstacles, as specified in range
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

    mob_list = ['😠', '🐷', '🤐', '😆', '😈', '😈', '😸', '🤓', '🌝', '😱', '😻']
    for i in range(8):  # generates as much mobs as specified in range
        x_generator = random.randrange(2, 28)
        y_generator = random.randrange(2, 78)
        random_mob = random.randrange(len(mob_list))
        insert_element(board, y_generator, x_generator, mob_list[random_mob])
        mob_list.pop(random_mob)


    item_list = ['🎽', '$', '💖', '🔪', '🔫']
    for i in range(2): # generates as much items as specified in range
        rand_pos_x = random.randrange(30, 79)
        rand_pos_y = random.randrange(10, 28)
        random_index = random.randrange(len(item_list))
        insert_element(board, rand_pos_x, rand_pos_y, item_list[random_index])
        item_list.pop(random_index)

    with open('map{}.txt'.format(level), 'w') as out:
        out.write('\n'.join(str(''.join(row)) for row in board))

    return board


def import_map(filename, level):
    '''Imports a map from a file(filename) for the given level and returns it'''
    map_to_import = []
    with open('map{}.txt'.format(level), 'r', newline='') as board:
        for row in board:
            map_to_import.append(list(row.rstrip('\n')))
    return map_to_import


def import_stats(filename):
    '''Imports a dictionary of stats from a file(filename) and returns it'''
    stats_dict = {}
    with open(filename, 'r') as stats:
        reader = csv.reader(stats, delimiter=',')
        for row in reader:
            stats_dict[row[0]] = int(row[1])

    return stats_dict


def export_stats(dictionary, filename):
    '''Exports all the stats from a given dictionary to a CSV file(filename)'''
    with open(filename, 'w') as stats:
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
    '''Returns a board with a player inserted in the given coordinations(width, height)'''
    board[height][width] = "@"
    return board


def insert_element(board, width, height, symbol):
    '''Returns a board with an element inserted in the given coordinations(width, height)'''
    board[height][width] = symbol
    return board


def x_movement(ch):
    '''Takes a character clicked as an argument and returns the x coordination of movement'''
    if ch == 'a':
        return -1
    elif ch == 'd':
        return 1
    else:
        return 0


def y_movement(ch):
    '''Takes a character clicked as an argument and returns the y coordination of movement'''
    if ch == 'w':
        return -1
    elif ch == 's':
        return 1
    else:
        return 0


def force_exit(ch):  # temporary exit feature for the testing phase
    if ch == 'q':
        exit()


def display_inventory(inventory, ch):
    '''Prints the inventory list under the board in a descending order.

        Args:
        inventory: a dictionary containing the items and their quantity
        ch: a character needed to trigger the print - here it's 'i'
    '''
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
        sorted_inventory = [(key, inventory[key]) for key in sorted(inventory, key=inventory.get, reverse=True)]
        for key, value in sorted_inventory:
            print('{:>7}{:{align}{width}}'.format(value, key, align='>', width=longest_string_count + 4))
        print('-' * (6 + len('count') + longest_string_count))
        print("Total number of items: {}".format(total_items))


def add_to_inventory(inventory, added_items):
    for item in added_items:
        if item in inventory:
            inventory[item] += 1
        else:
            inventory[item] = 1
    return inventory

def sub_from_inventory(inventory, sub_items):
    for item in sub_items:
        if item in inventory:
         inventory[item] -= 1
        else:
            inventory[item] = 0
    return inventory


def attack(board, ch, level, stats, x_player, y_player):
    '''Returns a board with attacks printed and updates the stats after every encounter.

        Args:
        board: the board coords at the moment of attack
        ch: a keyboard character clicked, here 'j' (for melee), 'k' (for ranged) and 'l' (for magic)
        level: a level of a current board
        stats: a dictionary containing all the stats readed from a CSV file
        x_player, y_player: coords of a player on a board
    '''
    if ch == 'j':
        try:
            for i in range(1, stats['strength'] + 1):  # the sword is as long as the strength value

                if not board[y_player][x_player + i] in ['😠', '🐷', '🤐', '😆', '😈', '😈', '😸', '🤓', '🌝', '😱', '😻']:
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
            for i in range(1, stats['dexterity'] + 1):  # the range is as long as dexteriy value

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
        if stats['energy'] > 0:  # the range is equal to energy, only mages can use it at the beginning
            if board[y_player + stats['energy']][x_player + stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player + stats['energy']][x_player + stats['energy']] = '*'
            if board[y_player][x_player + stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player][x_player + stats['energy']] = '*'
            if board[y_player - stats['energy']][x_player + stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player - stats['energy']][x_player + stats['energy']] = '*'
            if board[y_player + stats['energy']][x_player] not in ['X', '🏢', '→', '←']:
                board[y_player + stats['energy']][x_player] = '*'
            if board[y_player - stats['energy']][x_player] not in ['X', '🏢', '→', '←']:
                board[y_player - stats['energy']][x_player] = '*'
            if board[y_player - stats['energy']][x_player - stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player - stats['energy']][x_player - stats['energy']] = '*'
            if board[y_player][x_player - stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player][x_player - stats['energy']] = '*'
            if board[y_player + stats['energy']][x_player - stats['energy']] not in ['X', '🏢', '→', '←']:
                board[y_player + stats['energy']][x_player - stats['energy']] = '*'

    return board


def print_hall_of_fame(filename):
    with open(filename, 'r') as hall_of_fame:
        reader = csv.reader(hall_of_fame, delimiter=',')
        print("HALL OF FAME:")
        for row in reader:
            print(row)


def export_hall_of_fame(filename, stats, level, end_time):
    with open(filename, 'a') as hall_of_fame:
        writer = csv.writer(hall_of_fame, delimiter=',')
        writer.writerow(["Player name: {0}, Player class: {1}, Final stage: {2}, Time: {3}".format(player_name,
        player_class, level, end_time)])


def printed_attack_reset(board, level):
    '''UNDER CONSTRUCTION'''
    for row in board:
        for i in row:
            if i in ['-', '*', 'x']:
                i = '.'

    with open('map{}.txt'.format(level), 'w') as out:
        out.write('\n'.join(str(''.join(row)) for row in board))
    out.close()

    return board


def mob_movement(board, x_player, y_player, x_mob, y_mob, level):
    '''UNDER CONSTRUCTION!'''
    insert_player(board,x_player,y_player)
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
    import_map('map{}.txt'.format(level),level)
    return board

def print_boss():
    '''Prints the speaking Pikachu and redirects to cold-warm-hot game as a final challenge!'''
    os.system("clear")
    for i in range(5):
        print('''
    █▀▀▄░░░░░░░░░░░▄▀▀█
    ░█░░░▀▄░▄▄▄▄▄░▄▀░░░█
    ░░▀▄░░░▀░░░░░▀░░░▄▀
    ░░░░▌░▄▄░░░▄▄░▐▀▀
    ░░░▐░░█▄░░░▄█░░▌▄▄▀▀▀▀█
    ░░░▌▄▄▀▀░▄░▀▀▄▄▐░░░░░░█
    ▄▀▀▐▀▀░▄▄▄▄▄░▀▀▌▄▄▄░░░█
    █░░░▀▄░█░░░█░▄▀░░░░█▀▀▀
    ░▀▄░░▀░░▀▀▀░░▀░░░▄█▀
    ░░░█░░░░░░░░░░░▄▀▄░▀▄
    ░░░█░░░░░░░░░▄▀█░░█░░█
    ░░░█░░░░░░░░░░░█▄█░░▄▀
    ░░░█░░░░░░░░░░░████▀
    ░░░▀▄▄▀▀▄▄▀▀▄▄▄█▀''')
        sleep(0.4)
        os.system("clear")
        print('''
    █▀▀▄░░░░░░░░░░░▄▀▀█
    ░█░░░▀▄░▄▄▄▄▄░▄▀░░░█
    ░░▀▄░░░▀░░░░░▀░░░▄▀
    ░░░░▌░▄▄░░░▄▄░▐▀▀
    ░░░▐░░█▄░░░▄█░░▌▄▄▀▀▀▀█
    ░░░▌▄▄▀▀░▄░▀▀▄▄▐░░░░░░█
    ▄▀▀▐▀▀░▄▄▄▄▄░▀▀▌▄▄▄░░░█
    █░░░▀▄░█▀▀▀█░▄▀░░░░█▀▀▀
    ░▀▄░░▀░░░░░░░▀░░░▄█▀
    ░░░█░░░░░░░░░░░▄▀▄░▀▄
    ░░░█░░░░░░░░░▄▀█░░█░░█
    ░░░█░░░░░░░░░░░█▄█░░▄▀
    ░░░█░░░░░░░░░░░████▀
    ░░░▀▄▄▀▀▄▄▀▀▄▄▄█▀''')
        sleep(0.4)
        os.system("clear")
    hot_warm()


def main():
    level = 0
    board = create_board(80, 30, level)
    x_player = 1
    y_player = 1
    y_mob = random.randrange(2,28)
    x_mob = random.randrange(2,78)
    inventory = {}
    for i in range(levels_to_create):
        create_board(80, 30, i)

    item_list = {'🎽': 50,'$': 1,'🔪': 25,'🔫': 120,'💖': 1}
    cap_left = 510

    while True:
        character = getch()
        force_exit(character)
        stats = import_stats('stats.csv')
        board = insert_element(board, x_player, y_player, '.')
        with open('map{}.txt'.format(level), 'w') as out:
            out.write('\n'.join(str(''.join(row)) for row in board))
        board = import_map('map{}.txt'.format(level), level)
        x_player_before = x_player
        y_player_before = y_player
        if not board[y_player + y_movement(character)][x_player + x_movement(character)] in ['X','🏢','😠','🐷','🤐','😆','😈','😈','😸','🤓','🌝','😱','😻']:
            x_player = x_player + x_movement(character)
            y_player = y_player + y_movement(character)
        if board[y_player][x_player] == '→':
            x_player = 1
            y_player = 2
            level += 1
            board = import_map('map{}.txt'.format(level), level)
        if board[y_player][x_player] == '←':
            x_player = 78
            y_player = 5
            level -= 1
            board = import_map('map{}.txt'.format(level),level)
        if board[y_player][x_player] in item_list and item_list[board[y_player][x_player]] < cap_left:
            inventory = add_to_inventory(inventory,board[y_player][x_player])
            cap_left -= item_list[board[y_player][x_player]]
        elif board[y_player][x_player] in item_list and item_list[board[y_player][x_player]] > cap_left:
            x_player = x_player_before
            y_player = y_player_before
        # UNDER CONSTRUCTION: using potions
        # if character == 'p' and int(inventory['💖']) > 0:
        #     inventory['💖'] = int(inventory['💖']) -1
        #     inventory = sub_from_inventory(inventory,'💖')
        #     stats['life'] += int(stats['life']) + 1
        #     stats = import_stats('stats.csv')


        board_with_player = insert_player(board, x_player, y_player)
        # board_with_player = mob_movement(board, x_player, y_player, x_mob, y_mob, level)
        print_board(board_with_player)
        os.system('clear')
        print_board(attack(board, character, level, stats, x_player, y_player))
        display_inventory(inventory, character)
        print("Name: {0}, Class: {1}, Stage:{2}, Life:{3}, EXP:{4}, Str:{5}, Dex:{6}, Cap:{7}".format(
        player_name, player_class, level, stats['life'], stats['experience'], stats['strength'], stats['dexterity'],cap_left))

        if level == levels_to_create - 1:
            print_boss()
            end_time = int(time() - start_timer)
            export_hall_of_fame("hall_of_fame.csv", stats, level, end_time)
            print_hall_of_fame("hall_of_fame.csv")
            break

if __name__ == '__main__':
    main()
