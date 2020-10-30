import environment
import numpy as np
import Cell
import random
score = 0
n = 12
mines = 20

# print(board)
# for i in range(len(board)):
#     for j in range(len(board)):
#         print(board[i][j].covered, end=" ")
#     print()


def makeQuery(m, n, board):
    global hiddenBoard
    if(m<0 or n<0):
        return board
    if(m>=len(board.board) or n>=len(board.board)):
        return board
    query = environment.query(m, n, hiddenBoard)
    if query == -1:
        global score
        score+=1
        board = flag(m, n, board)
        return board
    board.board[m][n].isSafe=True
    board.board[m][n].covered=False
    board.board[m][n].mines=query
    board.makeSafe()
    board.makeHidden()
    board.makeMine()
    return board

def flag(m, n, board):
    if(m<0 or n<0):
        return board
    if(m>=len(board.board) or n>=len(board.board)):
        return board
    if board.board[m][n].isSafe == True:
        return board 
    board.board[m][n].isMine = True
    board.board[m][n].isSafe = False
    board.board[m][n].covered = False
    board.makeSafe()
    board.makeHidden()
    board.makeMine()
    board.board[m][n].mines = -1
    return board

# duv = 0

# hiddeBoard = 0
""" 
1. First we randomly query one cell
2. If it is 0 then we can open up all corresponding cells
3. clue - safe = hidden then every hidden neigbour is a mine 
4. if 8-clue - safe = hidden every hidden neighbour is safe
5. if cell is safe - isSafe is toggled and that spot is added
6. if cell is mine - use flag to flaf ir
7. Pick cell to reveal at random"""

def safeNator(mines, hidden, safe):
    if hidden == 0:
        return False
    if 8-mines-safe == hidden:
        return True
    else:
        return False

def mineNator(mines, hidden, minesIdentified):
    if hidden == 0:
        return False
    if mines-minesIdentified == hidden:
        return True
    else:
        return False


def isZero(m, n, board):
    # if(board.board[m][n])
    board = makeQuery(m-1, n, board)
    board = makeQuery(m-1, n-1, board)
    board = makeQuery(m-1, n+1, board)
    board = makeQuery(m, n+1, board)
    board = makeQuery(m, n-1, board)
    board = makeQuery(m+1, n-1, board)
    board = makeQuery(m+1, n+1, board)
    board = makeQuery(m+1, n, board)
    return board

def markMine(m, n, board):
    board = flag(m-1, n, board)
    board = flag(m-1, n-1, board)
    board = flag(m-1, n+1, board)
    board = flag(m, n+1, board)
    board = flag(m, n-1, board)
    board = flag(m+1, n-1, board)
    board = flag(m+1, n+1, board)
    board = flag(m+1, n, board)
    return board

def markSafe(m, n, board):
    if(m<0 or n<0):
        return board
    if(m>=len(board.board) or n>=len(board.board)):
        return board
    if board.board[m][n].isMine == True: # you don't want to querry mines
        return board
    board = makeQuery(m, n, board)
    # board.makeSafe()
    # board.makeHidden()
    # board.makeMine()
    return board

def safes(m, n, board): # you try it for everything
    board = markSafe(m-1, n, board)
    board = markSafe(m-1, n-1, board)
    board = markSafe(m-1, n+1, board)
    board = markSafe(m, n+1, board)
    board = markSafe(m, n-1, board)
    board = markSafe(m+1, n-1, board)
    board = markSafe(m+1, n+1, board)
    board = markSafe(m+1, n, board)
    return board

def check(n, board1): # this iterates over the whole board and find things that satisy the things, also check for zeroes
    flag = False
    for i in range(n):
        for j in range(n):
            # board1.makeSafe()
            # board1.makeHidden()
            # board1.makeMine()
            if(board1.board[i][j].mines==0):
                board1 = isZero(i, j, board1)
                # print("zeroes go off")
                # return board1
            elif mineNator(board1.board[i][j].mines, board1.board[i][j].hidden, board1.board[i][j].minesIdentified):
                # # print("minenator goes off")
                # print(str(i)+" and "+str(j))
                board1 = markMine(i, j, board1)
                return board1
            elif safeNator(board1.board[i][j].mines, board1.board[i][j].hidden, board1.board[i][j].safe):
                # print("safenator goes off")
                board1 = safes(i,j, board1)
                return board1
    # print("randoo")
    k = random.randint(0, n-1)
    l = random.randint(0, n-1)
    while(board1.board[k][l].covered==False):
        k = random.randint(0, n-1)
        l = random.randint(0, n-1)
    board1 = makeQuery(k,l,board1)
    return board1

def fin(n, board1):
    for i in range(n):
        for j in range(n):
            if(board1.board[i][j].covered==True):
                return True
    return False

def main(n, board1):
    """ 
    1. have a while loop to check if anything is bad
    2. get to checkch   
    3. If one is open and zero run is zero
    4. if minenator works - make mines
    5. If safenator takes off then safe takes off
    6. if nothing works do a random """
    # print(fin(n, board1))
    while(fin(n, board1)):
        board1 = check(n, board1)
    print("The score is")
    print((mines-score)/mines)
    return (mines-score)/mines
# print(hiddenBoard)
def checkMain(board, n):
    for i in range(n):
        for j in range(n):
            if(board.board[i][j].covered):
                return -1
            if(board.board[i][j].isMine==True):
                if hiddenBoard[i][j] ==-1:
                    print("cool")
                else:
                    print(i)
                    print(j)
                    return -2
# i=0
score1=0
hiddenBoard = environment.makeBoard(n, mines)
hiddenBoard = np.asarray(hiddenBoard)
print(hiddenBoard)
board1=Cell.Board(n)
# board1.printMine()
score1=main(n, board1)
# i+=1
# print(score1/1)
# print(board1.printIsMine())
# print(checkMain(board1, n))
# print(board1)
    # i+=1
# print(hiddenBoard)
# board1.printCovered()
# board1 = check(n, board1)



# print(hiddenBoard)
# board1 = Cell.Board(n)
# board1.printCovered()
# board1.printHidden()
# board1.printMines()
# board1.printSafe()
# board1 = makeQuery(0, 0, board1)
# board1.printCovered()
# board1.printHidden()
# board1.printMines()
# board1.printSafe()
# board1.printIsMine()
# board1.printHidden()
# board1.printCovered()
# board1.printIsMine()
# board1=makeQuery(0, 0, board1)
# board1.printMines() 
# board = np.zeros((len(hiddenBoard), len(hiddenBoard)))
# # Should i make a knowledge base board??
# for i in range(len(board)):
#     for j in range(len(board)):
#         board[i][j]=-3
# # print(board)
# while (duv != 2):
#     inp = input()
#     operation=inp.split()[0]
#     m = inp.split()[1]
#     n = inp.split()[2]
#     # print(m + " " + n)
#     if operation == "q":
#         makeQuery(int(m), int(n), board)
#         print(board)
#         duv += 1
#     if operation == "f":
#         flag(int(m), int(n), board)
#         print(board)
#         duv += 1

