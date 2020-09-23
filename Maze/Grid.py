import numpy as np
import random


class Map:
    def __init__(self, dim):  # will know the prob of each maze
        self.dim = dim
        self.map1 = np.zeros((dim, dim))

    # populates map with 0s and 1s for blocked and free cells respectively. 2 indicates start and 3 indicates finish

    def populate(self, p):
        if p > 1 or p < 0:
            raise ValueError("Probability must be between 0 and 1")
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

    def isBlocked(self, x, y):
        # Checks if square is blocked
        if self.map1[x][y] == 0:
            print("Blocked")
        if self.map1[x][y] == 1:
            print("Not Blocked")

    def legal(self, x, y):
        # Checks if square is out of bounds of map
        if 0 <= x < self.dim and 0 <= y < self.dim:
            return True
        else:
            return False

    def trace(self, traceSet, x, y):
        final = (x, y)
        stack = [final]
        back = traceSet[final]

        while back is not None:
            stack.append(back)
            back = traceSet[back]
            # print(back)
        return stack

    def printStack(self, stack):
        for i in range(len(stack)):
            print(stack.pop())

    def savePath(self, stack):  # also prints stack but saves the BFS path
        path = []
        for i in range(len(stack)):
            x = stack.pop()
            path.append(x)
            # print(x) #Prints the path after saving it
        return path

    # adds random fire to the map

    def addFire(self):
        dom = self.dim * self.dim
        prob = 1 / dom
        flag = False
        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.map1[x][y] == 0 or self.map1[x][y] == 2 or self.map1[x][y] == 3:
                    continue
                if self.map1[x][y] == 1:
                    if random.random() < prob:
                        self.map1[x][y] = 4
                        self.firex = x
                        self.firey = y
                        return
                    else:
                        dom -= 1
                        prob = 1 / dom
        self.addFire()

    # gets a list of free squares on the map (squares with value of 1)

    def getFreeSquares(self):
        ans = []
        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.map1[x][y] == 1:
                    cord = (x, y)
                    ans.append(cord)
        return ans

    # gets a list of squares on the map that are on fire (squares with value of 4)

    def getSquaresOnFire(self):

        ans = []

        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.map1[x][y] == 4:
                    cord = (x, y)
                    ans.append(cord)
        return ans

    # gets a list of squares that will be set on fire in the next turn

    def getFireSet(self, q, freeSquares):

        freeSquares = self.getFreeSquares()
        length = len(freeSquares)
        fire_set = []

        for i in range(0, length):
            adj = []
            neighbors = []
            burning_neighbors = 0
            adj = self.getAdj(freeSquares[i][0], freeSquares[i][1])
            adj_length = len(adj)
            for j in range(0, adj_length):
                if self.legal(adj[j][0], adj[j][1]):
                    neighbors.append(adj[j])
            neighbors_length = len(neighbors)
            for k in range(0, neighbors_length):
                x_cord = neighbors[k][0]
                y_cord = neighbors[k][1]
                if self.map1[x_cord][y_cord] == 4:
                    burning_neighbors += 1
            power = pow(1 - q, burning_neighbors)
            prob_on_fire = 1 - power
            if random.random() < prob_on_fire:
                fire_set.append(freeSquares[i])



        return fire_set

    # spreads fire to squares in fire set (sets squares value to 4)

    def spreadFire(self, fire_set):

        length = len(fire_set)

        for i in range(0, length):
            x_cord = fire_set[i][0]
            y_cord = fire_set[i][1]
            self.map1[x_cord][y_cord] = 4

    def bfs(self, queue, target, targetx,
            targety):  # finds BFS path to the finish. if there is no path, will return nothing

        """You start will the beginning
        1. Get all the adjacents
        2. Check whats legal
        3. If legal check the set
        4. If does not exist in set can add to the queue"""

        '''
        1. So we have a parent matrix
        2. This records the parent
        3. We have a dictionary of cell: parents'''

        thisset = {(0, 0)}
        traceSet = {(0, 0): None}

        flag = False  # variable to see if it is possible to reach the goal
        while queue:
            fringe = queue.pop(0)  # gets 0, 0 first
            adjs = self.getAdj(fringe[0], fringe[1])

            if self.map1[fringe[0]][fringe[1]] == 2:
                print("Our attempt has started")

            if self.map1[fringe[0]][fringe[1]] == target:
                print("Goal reached")
                print("This is how you go about it")
                # print(traceSet)
                ans = self.trace(traceSet, targetx, targety)
                path = self.savePath(ans)
                flag = True
                # print(ans.pop())
                break

            if self.map1[fringe[0]][fringe[1]] == 0 or self.map1[fringe[0]][fringe[1]] == 3:
                continue

            for i in range(len(adjs)):
                if self.legal(adjs[i][0], adjs[i][1]):
                    if adjs[i] in thisset:
                        continue

                    thisset.add(adjs[i])
                    traceSet[adjs[i]] = fringe
                    queue.append(adjs[i])
        if flag is False:
            print("No way to goal")
            return []
        return path


m1 = Map(100)  # dimensions
m1.populate(0.2)  # populates using parameter prob
print("Path to Finish")
BFSpathTarget = m1.bfs([(0, 0)], 3, m1.dim - 1,
                       m1.dim - 1)  # finds path to the finish. if there isn't one, it will say so
print(BFSpathTarget)
m1.addFire()  # adds random fire to free cell in map
print("Map with random first fire placed")
print(m1.map1)
print("Path to Fire")
BFSpathFire = m1.bfs([(0, 0)], 4, m1.firex, m1.firey)  # finds path to the fire, if there isn't one, it will say so



#Assuming there is a path to the fire now what do we do




fireList = []
for i in range(len(BFSpathTarget)):
    fireSet1 = m1.getSquaresOnFire()
    fireList.append(fireSet1)
    freeSquares = m1.getFreeSquares()  # gets free squares after fire has been placed
    fireSet = m1.getFireSet(1, freeSquares)  # list of squares that will be set on fire after 1 turn
    # print("Fire Set: ", fireSet)
    m1.spreadFire(fireSet)  # spreads the fire



print(len(fireList))
print(len(BFSpathTarget))


for i in range(len(fireList)):
    if BFSpathTarget[i] in fireList[i]:
        print("Fire Fire Fire Fire Fire")
        break
# print("New Map with Fire after 1 turn")
# # print(m1.map1)
# freeSquares2 = m1.getFreeSquares()  # gets free squares after fire has spread 1 turn
# fireSet2 = m1.getFireSet(1, freeSquares2)  # list of squares that will be set on fire after 2 turns
# print("Fire Set 2: ", fireSet2)
# m1.spreadFire(fireSet2)  # spreads the fire again
# print("New Map with Fire after 2 turns")
# print(m1.map1)

# mat = np.random.random((100, 100))
# Creates PIL image

# for x in range(0, m1.dim):
#     for y in range(0, m1.dim):
#         if m1.map1[x][y] == 2:
#             m1.map1[x][y]=1
#         if m1.map1[x][y] == 3:
#             m1.map1[x][y]=1
#         if m1.map1[x][y] == 1:
#             m1.map1[x][y]=10
#         if m1.map1[x][y] == 0:
#             m1.map1[x][y]=1
#         if m1.map1[x][y] == 10:
#             m1.map1[x][y]=0

# print(m1.map1)
# img = Image.fromarray(m1.map1, 'L')
# img.show()