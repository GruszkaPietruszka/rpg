import random
from time import sleep
import os


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


def print_inventory(item_to_add):
    pass


def create_board(width, height,door_pos=19):
    board = []
    line = 0
    #For door position:
     # odd for arrow on right side,
    middle_door = 0 # even for arrow on left side
    for row in range(0, height):
        board_row = []
        for column in range(0, width):
            if row == 0 or row == height-1:
                board_row.append("X")
            else:   #if column == 0 or column == width - 1:
                if column == 0 or column == width -1:
                    if door_pos != middle_door:
                        board_row.append("X")
                        middle_door +=  1
                    else:
                        if door_pos % 2 == 0:
                            board_row.append("⭁")
                            middle_door += 1
                        else:
                            board_row.append("⭌")
                            middle_door += 1
                else:
                    board_row.append(".")
        board.append(board_row)

    for i in range(15):
        x_generator = random.randrange(5,25)
        y_generator = random.randrange(5,75)
        board[x_generator][y_generator] = 'X'
        board[x_generator-1][y_generator] = 'X'
        board[x_generator+1][y_generator] = 'X'
        board[x_generator][y_generator+1] = 'X'
        board[x_generator][y_generator-1] = 'X'
        board[x_generator-1][y_generator-1] = 'X'
        board[x_generator+1][y_generator+1] = 'X'
        board[x_generator+1][y_generator-1] = 'X'
        board[x_generator-1][y_generator+1] = 'X'

    with open('maps.txt', 'w') as out:
        out.write('\n'.join(str(''.join(row)) for row in board))

    #with open(maps.txt, 'w') as out:
        #out.write('\n'.join(str(''.join(row)) for row in board))

    return board


def import_map(filename):
    map_one = []
    with open('maps.txt', 'r', newline='') as board:
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


def insert_mob(board, width, height):
    board[height][width] = 'X'
    return board

def export_pos_of_lands():
    pass


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
    board = create_board(80,30)

    x_player = 1
    y_player = 1
    life = 5
    inventory = []

    while True:
        character = getch()
        force_exit(character)
        os.system('clear')
        board = import_map('maps.txt')
        #board_with_player = insert_mob(board, 5, 5)
        if not board[y_player + y_movement(character)][x_player + x_movement(character)] == 'X':
            x_player = x_player + x_movement(character)
            y_player = y_player + y_movement(character)
        board_with_player = insert_player(board, x_player, y_player)
        print_board(board_with_player)

        print("Life:", str(''.join(health(life)))), "Inventory:", str(' '.join(inventory[0:]))


main()
