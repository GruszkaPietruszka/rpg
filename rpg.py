from random import randint
from time import sleep
import os


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
                    board_row.append(" ")
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


def main():
    width = int(input("Write the width value: "))
    height = int(input("Write the height value: "))
    for step in range(0, 10):
        os.system('clear')
        board = create_board(height, width)
        board_with_player = insert_player(board, 5 + step, 15)
        print_board(board_with_player)
        sleep(0.1)


main()
