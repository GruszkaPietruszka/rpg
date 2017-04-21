from random import randint
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


def create_board(width, height):
    board = []

    for row in range(0, height):
        board_row = []
        for column in range(0, width):
            if row == 0 or row == height-1:
                board_row.append("X")
            else:
                if column == 0 or column == width - 1:
                    board_row.append("X")
                else:
                    board_row.append(".")
        board.append(board_row)

    return board


def print_board(board):
    for row in board:
        for char in row:
            print(char, end='')
        print()


def insert_player(board, width, height):
    board[height][width] = '@'
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


def main():
    x_position = 15
    y_position = 15
    while True:
        character = getch()
        force_exit(character)
        os.system('clear')
        board = create_board(120, 40)
        if not board[y_position + y_movement(character)][x_position + x_movement(character)] == 'X':
            board_with_player = insert_player(board, x_position + x_movement(character), y_position + y_movement(character))
            x_position = x_position + x_movement(character)
            y_position = y_position + y_movement(character)
            print_board(board_with_player)
        else:
            print_board(board_with_player)


main()
