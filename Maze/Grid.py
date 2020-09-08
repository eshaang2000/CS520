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
                if x == 0 and y == 0:
                    self.map1[x][y] = 2
                    continue
                if x == self.dim - 1 and y == self.dim - 1:
                    self.map1[x][y] = 3
                    continue

                if random.random() < p:
                    self.map1[x][y] = 0
                    zeroes += 1
                else:
                    ones += 1
                    self.map1[x][y] = 1
        # print(ones)
        # print(zeroes)
        print(self.map1)

    def getAdj(self, x, y):
        # get the adjacent indices
        # the possible movements are up, down, right, and left
        ans = []
        right = (x, y + 1)
        left = (x, y - 1)
        up = (x - 1, y)
        down = (x + 1, y)
        ans.append(right)
        ans.append(left)
        ans.append(up)
        ans.append(down)
        return ans
        # now check if these coordinates are legal or not
        # if self.legal(right[0], right[1]):
        #     print("Right is cool")
        # else:
        #     print("Right is NOT cool")
        #
        # if self.legal(left[0], left[1]):
        #     print("Left is cool")
        # else:
        #     print("Left is NOT cool")
        #
        # if self.legal(up[0], up[1]):
        #     print("Up is cool")
        # else:
        #     print("Up is NOT cool")
        #
        # if self.legal(down[0], down[1]):
        #     print("Down is cool")
        # else:
        #     print("Down is NOT cool")

    def isBlocked(self, x, y):
        # Checks if square is blocked
        if self.map1[x][y] == 0:
            print("Blocked")
        if self.map1[x][y] == 1:
            print("Not Blocked")

    def legal(self, x, y):
        if 0 <= x < self.dim and 0 <= y < self.dim:
            return True
        else:
            return False

    def bfs(self, queue):
        # queue = [(0, 0)] # you start with
        '''You start will the beginning
        1. Get all the adjacents
        2. Check whats legal
        3. If legal check the set
        4. If does not exist in set can add to the queue'''
        thisset = {(0,0)}
        while queue:
            fringe = queue.pop(0)  ##gets 0, 0 first
            adjs = self.getAdj(fringe[0], fringe[1])

            if self.map1[fringe[0]][fringe[1]] == 2:
                print("initial reached")

            if self.map1[fringe[0]][fringe[1]] == 3:
                print("Goal reached")

            if self.map1[fringe[0]][fringe[1]] == 0:
                continue

            # print("The adjacents")
            # print(adjs[0][0])
            # print(adjs)
            for i in range(len(adjs)):

                if self.legal(adjs[i][0], adjs[i][1]):
                    if adjs[i] in thisset:
                        continue

                    thisset.add(adjs[i])
                    print(adjs[i])
                    queue.append(adjs[i])


m1 = Map(5)  # dimensions
m1.populate(0.3)  # populTES Usind parameter prob
# m1.getAdj(1, 0)
# m1.isBlocked(1,0)
# print(m1.legal(-1, 0))
m1.bfs([(0, 0)])
# print(m1.map1[1][0])
# print(m1.map1)
# print(random.random())
