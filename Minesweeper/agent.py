import environment
import numpy as np
import Cell

n = 4
mines = 3

# print(board)
# for i in range(len(board)):
#     for j in range(len(board)):
#         print(board[i][j].covered, end=" ")
#     print()


def makeQuery(m, n, board):
    if(m<0 or n<0):
        return board
    if(m>=len(board.board) or n>=len(board.board)):
        return board
    query = environment.query(m, n, hiddenBoard)
    if query == -1:
        print("Boom")
        exit()
    board.board[m][n].isSafe=True
    board.board[m][n].covered=False
    board.board[m][n].mines=query
    board.board[m][n].hidden=board.findHidden(m, n)
    board.board[m][n].safe=board.findSafe(m,n)
    return board

def flag(m, n, board):
    if(m<0 or n<0):
        return board
    if(m>=len(board.board) or n>=len(board.board)):
        return board
    if board.board[m][n].isSafe == False:
        return board 
    board.board[m][n].isMine = True
    board.board[m][n].isSafe = False
    return board

duv = 0
hiddenBoard = environment.makeBoard(n, mines)
hiddenBoard = np.asarray(hiddenBoard)

""" 
1. First we randomly query one cell
2. If it is 0 then we can open up all corresponding cells
3. clue - safe = hidden then every hidden neigbour is a mine 
4. if 8-clue - safe = hidden every hidden neighbour is safe
5. if cell is safe - isSafe is toggled and that spot is added
6. if cell is mine - use flag to flaf ir
7. Pick cell to reveal at random"""

def safeNator(mines, hidden, safe):
    if 8 - mines-safe == hidden:
        return True
    else:
        return False

def mineNator(mines, hidden, safe):
    if mines-safe == hidden:
        return True
    else:
        return False


def isZero(m, n, board):
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
    if board.board[m][n].isSafe == False:
        return board
    query = environment.query(m, n, hiddenBoard)
    if query == -1:
        print("Boom")
        exit()
    board.board[m][n].isSafe=True
    board.board[m][n].covered=False
    board.board[m][n].mines=query
    board.board[m][n].hidden=board.findHidden(m, n)
    board.board[m][n].safe=board.findSafe(m,n)
    return board

def safes(m, n, board):
    board = markSafe(m-1, n, board)
    board = markSafe(m-1, n-1, board)
    board = markSafe(m-1, n+1, board)
    board = markSafe(m, n+1, board)
    board = markSafe(m, n-1, board)
    board = markSafe(m+1, n-1, board)
    board = markSafe(m+1, n+1, board)
    board = markSafe(m+1, n, board)
    return board








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

