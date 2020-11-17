import numpy as np
import random


class Landscape:
    def __init__(self, map1, dim):
        self.map1 = np.zeros((dim, dim))
        self.dim = dim
        self.target = (0, 0)  # initial value of the target

    def populate(self):
        x = random.randint(0, self.dim-1)
        y = random.randint(0, self.dim-1)
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
        #If we reach here then the target is present here
            rando = random.random()
        if self.map1[x][y] == 1:
            if rando < 0.1:
                return False
        elif self.map1[x][y] == 2:
            if rando < 0.3:
                return False
        elif self.map1[x][y] == 3:
            if rando < 0.7:
                return False
        elif self.map1[x][y] == 4:
            if rando < 0.9:
                return False


    def queryTerrainType(self, x, y):
        return self.map1[x][y]
