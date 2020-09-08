import numpy as np
import random


class Map:
    def __init__(self, dim):  # will know the prob of each maze
        self.dim = dim
        # self.p = p

        # if p > 1 or p < 0:
        #     raise ValueError("Probability must be between 0 and 1")
        self.map1 = np.zeros((dim, dim))

    def populate(self, p):
        # print(self.map1)
        ones = 0
        zeroes = 0
        # print(self.dim)
        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if x==0 and y==0:
                    self.map1[x][y]=2
                    continue
                if x == self.dim-1 and y == self.dim-1:
                    self.map1[x][y] = 3
                    continue

                if(random.random()<p):
                    self.map1[x][y]=0
                    zeroes+=1
                else:
                    ones+=1
                    self.map1[x][y]=1
        # print(ones)
        # print(zeroes)
        print(self.map1)
    def getAdj(self, x, y):
        #get the adjacent indices
        print("Eshaan")
    def bfs(self):
        queue = []
        queue.append((0,0))

        # seen = set([start])

        

m1 = Map(5)
m1.populate(0.3)
m1.bfs()
# print(m1.map1)
# print(random.random())