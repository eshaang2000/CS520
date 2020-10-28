import numpy as np
class Cell:
    def __init__(self):
        super().__init__()
        self.covered = True
        self.mines = 0
        self.hidden = 0
        self.safe = 0
        self.isMine = False
        self.isSafe = False

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
    
    def isSafe(self, m, n):
        if m<0 or n<0:
            return 0
        if m>=len(self.board) or n>=len(self.board):
            return 0
        if self.board[m][n].isSafe == True:
            return 1
        return 0

    def findSafe(self, m, n):
        ans = 0
        ans+=self.isSafe(m+1, n)
        ans+=self.isSafe(m-1, n)
        ans+=self.isSafe(m+1, n+1)
        ans+=self.isSafe(m-1, n-1)
        ans+=self.isSafe(m, n+1)
        ans+=self.isSafe(m, n-1)
        ans+=self.isSafe(m+1, n-1)
        ans+=self.isSafe(m-1, n+1)
        self.board[m][n].safe=ans
    

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
                print(self.board[i][j].hidden, end=" ")
            print()

    def printSafe(self):
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                print(self.board[i][j].safe, end=" ")
            print()

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