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


def create_board(width, height):
    board = []
    line = 0

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

    with open('map.txt', 'r') as maps:
        for row in maps:
            line += 1
            if line % 2 == 0:
                x_generator = row
            else:
                y_generator = row

    x_generator = int(x_generator)
    y_generator = int(y_generator)
    board[x_generator][y_generator] = 'X'
    board[x_generator-1][y_generator] = 'A'
    board[x_generator+1][y_generator] = 'B'
    board[x_generator][y_generator+1] = 'C'
    board[x_generator][y_generator-1] = 'D'
    board[x_generator-1][y_generator-1] = 'E'
    board[x_generator+1][y_generator+1] = 'F'
    board[x_generator+1][y_generator-1] = 'G'
    board[x_generator-1][y_generator+1] = 'H'




    #board = create_lands(board,width,height)

    return board


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

def generate_lands(width, height, count = 5):
    y_generator = random.randrange(0,width)
    x_generator = random.randrange(0,height)

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
    x_position = 15
    y_position = 15
    life = 5
    inventory = []
    #board = create_board(80,30)
    generate_lands(25,25)

    while True:
        character = getch()
        force_exit(character)
        os.system('clear')
        board = create_board(80,30)
        board_with_player = insert_mob(board,5,5)
        if not board[y_position + y_movement(character)][x_position + x_movement(character)] == 'X':
            x_position = x_position + x_movement(character)
            y_position = y_position + y_movement(character)
        board_with_player = insert_player(board, x_position, y_position)
        print_board(board_with_player)






        print("Life:", str(''.join(health(life)))), "Inventory:", str(' '.join(inventory[0:]))


main()
