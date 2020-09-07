import numpy as np

class Map:
    def __init__(self, dim, p): #will know the prob of each maze
        self.dim = dim
        self.p = p

        if p > 1 or p < 0:
            raise ValueError("Probability must be between 0 and 1")
        map1 = np.zeros((dim, dim))
        print(map1)


m1 = Map(10, .5)

    # def make:

