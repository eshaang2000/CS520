import random
import numpy as np


# 1. Make a grid - done
# 2. put the mines
# 3. Set the values
# 4. I guess we are ready to rumble then - done
# Printing the Minesweeper Layout

def makeGrid(n):
    numbers1 = [[0 for y in range(n)] for x in range(n)]
    return numbers1

def set_mines(numbers1, mines_no, n):
    count = 0
    while count < mines_no:
        # Random number from all possible grid positions
        # val = random.randint(0, n * n - 1)
        # Generating row and column from the number
        r = random.randint(0, n-1)
        col = random.randint(0, n-1)

        if numbers1[r][col] != -1:
            count = count + 1
            numbers1[r][col] = -1
    return numbers1


# Function for setting up the other grid values
def set_values(numbers1, n):
    # Loop for counting each cell value
    for r in range(n):
        for col in range(n):

            # Skip, if it contains a mine
            if numbers1[r][col] == -1:
                continue

            # Check up
            if r > 0 and numbers1[r - 1][col] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check down
            if r < n - 1 and numbers1[r + 1][col] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check left
            if col > 0 and numbers1[r][col - 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check right
            if col < n - 1 and numbers1[r][col + 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check top-left
            if r > 0 and col > 0 and numbers1[r - 1][col - 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check top-right
            if r > 0 and col < n - 1 and numbers1[r - 1][col + 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check below-left
            if r < n - 1 and col > 0 and numbers1[r + 1][col - 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
            # Check below-right
            if r < n - 1 and col < n - 1 and numbers1[r + 1][col + 1] == -1:
                numbers1[r][col] = numbers1[r][col] + 1
    return numbers1


def printGrid(numbers1, n):
    for i in range(n):
        for j in range(n):
            print(numbers1[i][j], end=' ')
        print()

def query(m, n, numbers):
    return numbers[m][n]

def makeBoard(n, mines):
    numbers = makeGrid(n)
    numbers = set_mines(numbers, mines, n)
    numbers = set_values(numbers, n)
    return numbers

