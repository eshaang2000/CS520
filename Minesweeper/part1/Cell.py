import numpy as np
class Cell:
    def __init__(self):
        # super().__init__()
        self.covered = True #Boolean value that is covered 
        self.mines = -10 #Number of mines around
        self.minesIdentified = 0 # number of mines that are identified around a cell
        self.hidden = 0 #Number of hidden cells around current cell
        self.safe = 0 #number of cells that are uncovered and are safe
        self.isMine = False #boolean value that tells you if the player has flagged it
        self.isSafe = False #if opened and not a mine

class Board:
    def __init__(self, n):
        # super().__init__()
        # n=8
        self.n=n
        self.board = [[Cell() for j in range(self.n)] for i in range(self.n)]
        # print(board[0][0])

    # def create(self, n):
        
    #     return board

    def isHidden(self, m, n):
        if m<0 or n<0:
            return 0
        if m>=len(self.board) or n>=len(self.board):
            return 0
        if self.board[m][n].covered == True:
            return 1
        return 0

    def findHidden(self, m, n):
        ans = 0
        ans+=self.isHidden(m+1, n)
        ans+=self.isHidden(m+1, n+1)
        ans+=self.isHidden(m-1, n)
        ans+=self.isHidden(m-1, n-1)
        ans+=self.isHidden(m, n+1)
        ans+=self.isHidden(m, n-1)
        ans+=self.isHidden(m+1, n-1)
        ans+=self.isHidden(m-1, n+1)
        self.board[m][n].hidden=ans
    
    def isSafe1(self, m, n):
        if m<0 or n<0:
            return 0
        if m>=len(self.board) or n>=len(self.board):
            return 0
        if self.board[m][n].isSafe == True:
            return 1
        return 0

    def findSafe(self, m, n):
        ans = 0
        ans+=self.isSafe1(m-1, n)
        ans+=self.isSafe1(m+1, n)
        ans+=self.isSafe1(m+1, n+1)
        ans+=self.isSafe1(m-1, n-1)
        ans+=self.isSafe1(m, n+1)
        ans+=self.isSafe1(m, n-1)
        ans+=self.isSafe1(m+1, n-1)
        ans+=self.isSafe1(m-1, n+1)
        self.board[m][n].safe=ans

    def isMine1(self, m, n):
        if m<0 or n<0:
            return 0
        if m>=len(self.board) or n>=len(self.board):
            return 0
        if self.board[m][n].isMine == True:
            return 1
        return 0

    def findMine(self, m, n):
        ans = 0
        ans+=self.isMine1(m-1, n)
        ans+=self.isMine1(m+1, n)
        ans+=self.isMine1(m+1, n+1)
        ans+=self.isMine1(m-1, n-1)
        ans+=self.isMine1(m, n+1)
        ans+=self.isMine1(m, n-1)
        ans+=self.isMine1(m+1, n-1)
        ans+=self.isMine1(m-1, n+1)
        self.board[m][n].minesIdentified=ans
    

    def printCovered(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j].covered, end=" ")
            print()
    
    def printMines(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j].mines, end=" ")
            print()

    def printHidden(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findHidden(i, j)
                print(self.board[i][j].hidden, end=" ")
            print()

    def printSafe(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findSafe(i,j)
                print(self.board[i][j].safe, end=" ")
            print()

    def printMine(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findMine(i,j)
                print(self.board[i][j].minesIdentified, end=" ")
            print()

    def makeHidden(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findHidden(i, j)
                # print(self.board[i][j].hidden, end=" ")
            # print()

    def makeSafe(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findSafe(i,j)
                # print(self.board[i][j].safe, end=" ")
            # print()

    def makeMine(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                self.findMine(i,j)
                # print(self.board[i][j].minesIdentified, end=" ")
            # print()

    def printIsMine(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j].isMine, end=" ")
            print()
    
    
    


# print(b.findHidden(0,0))
# b = Board().create(8)
# for i in range(len(b)):
#     for j in range(len(b)):
#         print(b[i][j].covered, end=" ")
#     print()
# print(b.create(8)[0][0].covered)