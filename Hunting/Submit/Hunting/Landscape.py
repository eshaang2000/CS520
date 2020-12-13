import numpy as np
import random


class Landscape:
    def __init__(self, dim):
        self.dim = dim
        self.map1 = np.zeros((dim, dim))
        self.target = (0, 0)  # initial value of the target
        self.populate()

    def setNewTarget(self):
        x = random.randint(0, self.dim - 1)
        y = random.randint(0, self.dim - 1)
        self.target = (x, y)

    def populate(self):
        x = random.randint(0, self.dim - 1)
        y = random.randint(0, self.dim - 1)
        self.target = (x, y)
        for i in range(self.dim):
            for j in range(self.dim):
                rando = random.random()
                if rando < 0.2:
                    self.map1[i][j] = 1
                elif rando < 0.5:
                    self.map1[i][j] = 2
                elif rando < 0.8:
                    self.map1[i][j] = 3
                else:
                    self.map1[i][j] = 4

    def query(self, x, y):
        if self.target[0] != x or self.target[1] != y:
            return False
        # If we reach here then the target is present here
        randNo = random.random()
        if self.map1[x][y] == 1:
            if randNo < 0.1:
                return False
        elif self.map1[x][y] == 2:
            if randNo < 0.3:
                return False
        elif self.map1[x][y] == 3:
            if randNo < 0.7:
                return False
        elif self.map1[x][y] == 4:
            if randNo < 0.9:
                return False
        return True

    def queryTerrainType(self, x, y):
        if self.map1[x][y] == 1:
            return 0.1
        elif self.map1[x][y] == 2:
            return 0.3
        elif self.map1[x][y] == 3:
            return 0.7
        elif self.map1[x][y] == 4:
            return 0.9
        else:
            return 0

    def queryTerrain(self, x, y):
        if self.map1[x][y] == 1:
            return 1
        elif self.map1[x][y] == 2:
            return 2
        elif self.map1[x][y] == 3:
            return 3
        elif self.map1[x][y] == 4:
            return 4
        else:
            return 0

    def printMap(self):
        print(self.map1)

    def printTarget(self):
        print(self.target)
