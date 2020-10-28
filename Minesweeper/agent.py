import environment
import numpy as np
import Cell

n = 4
mines = 3
hiddenBoard = environment.makeBoard(n, mines)
print(np.asarray(hiddenBoard))
board1 = Cell.Board(n)
print(len(board1.board))
# print(board)
# for i in range(len(board)):
#     for j in range(len(board)):
#         print(board[i][j].covered, end=" ")
#     print()


def makeQuery(m, n, board):
    query = environment.query(m, n, hiddenBoard)
    if query == -1:
        print("Boom")
        exit()
    board.board[m][n].isSafe=True
    board.board[m][n].covered=False
    board.board[m][n].mines = query
    board.board[m][n].hidden=board.findHidden(m, n)
    board.board[m][n].safe=board.findSafe(m,n)
    return board

def flag(m, n, board):
    board[m][n].isMine = True
    return board

duv = 0
# board1.printHidden()
board1=makeQuery(0, 0, board1)
board1.printMines() 
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

