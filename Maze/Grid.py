import numpy as np
import random


class Map:
    def __init__(self, dim):  # will know the prob of each maze
        self.dim = dim
        # self.p = p

        # if p > 1 or p < 0:
        #     raise ValueError("Probability must be between 0 and 1")
        self.map1 = np.zeros((dim, dim))

    def populate(self,p):
        for i in self.map1:
            for j in self.map1:
                i=5
                print(i)
                print(j)


m1 = Map(10)
m1.populate(0.5)
print(m1.map1)
# print(random.random())
