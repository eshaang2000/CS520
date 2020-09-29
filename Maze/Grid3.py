import numpy as np
import random
import math
import copy
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

        thisset = {queue[0]}
        traceSet = {queue[0]: None}

        flag = False  # variable to see if it is possible to reach the goal
        while queue:
            fringe = queue.pop(0)  # gets 0, 0 first
            adjs = self.getAdj(fringe[0], fringe[1])

            if self.map1[fringe[0]][fringe[1]] == 2:
                print("Our attempt has started")

            if self.map1[fringe[0]][fringe[1]] == target:
                ans = self.trace(traceSet, targetx, targety)
                path = self.savePath(ans)
                flag = True
                # print("Goal reached")
                # print("This is how you go about it")
                # print(traceSet)
                # print(ans.pop())
                break

            if self.map1[fringe[0]][fringe[1]] == 0 or self.map1[fringe[0]][fringe[1]] == 3 or self.map1[fringe[0]][fringe[1]] == 4:
                continue

            for i in range(len(adjs)):
                if self.legal(adjs[i][0], adjs[i][1]):
                    if adjs[i] in thisset:
                        continue

                    thisset.add(adjs[i])
                    traceSet[adjs[i]] = fringe
                    queue.append(adjs[i])
        if flag is False:
            # print("No way to goal")
            return []
        return path
    def fireUtility(self, x, y):
        sum = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.map1[i][j] == 4:
                    sum += (abs(x - i) + abs(y - j))
        return sum
    def distanceUtility(self, x, y):
        ans = (x-self.dim-1)**2+(y-self.dim-1)**2
        ans = math.sqrt(ans)
        return ans

    # def localSearch(self, queue, target, dimx, dimy):
    #     """
    #     You start will the beginning
    #     1. Get all the adjacents
    #     2. Check whats legal
    #     3. If legal check the set
    #     4. If does not exist in set can add to the queue
    #     """
    #     s = (0,0)
        
    #     counter = 0
    #     while(counter<1000):
    #         adjs = self.getAdj(s[0], s[1])
    #         minD = 10000
    #         min = (0,0)
    #         for i in adjs:
    #             if self.distanceUtility(i[0], i[1]) < min:
    #                 min = i
    #         s = min
    #     print("poop")

def sim(length, m1, qu, start):
    """ 
    1. At this point all bottlenecks are fulfilled
    2. We want to simulate 1/5 of the maze and find a BFS path
    3. This function returns that BFS Path
    """
    msim = copy.deepcopy(m1)
    for i in range(8): #int(math.floor(float(length))/5)
        # fireSet1 = m1.getSquaresOnFire()
        # fireList.append(fireSet1)
        freeSquares = msim.getFreeSquares()  # gets free squares after fire has been placed
        fireSet = msim.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
        # print("Fire Set: ", fireSet)
        msim.spreadFire(fireSet)
    print(msim.map1)
    print("here")
    print(start)
    BFSpathTarget2 = msim.bfs([start], 3, m1.dim - 1, m1.dim - 1)
    return BFSpathTarget2[0:8]


def test(qu):
    m1 = Map(10)  # dimensions
    # msim = Map(10)
    m1.populate(0.3)  # populates using parameter prob
   
    #print("Path to Finish")
    BFSpathTarget = m1.bfs([(0, 0)], 3, m1.dim - 1,
                        m1.dim - 1)  # finds path to the finish. if there isn't one, it will say so

    if BFSpathTarget==[]:
        return -1 #Bottleneck failed
    m1.addFire()
    
    BFSpathFire = m1.bfs([(0, 0)], 4, m1.firex, m1.firey)  # finds path to the fire, if there isn't one, it will say so
    if BFSpathFire==[]:
        return -1 # Bottle neck failed
    # msim = copy.deepcopy(m1)
    #print(BFSpathFire)

    #Assuming there is a path to the fire now what do we do
    """ 
    1. All the bottle necks are past
    2. Simulate the fire and see if there is a path """


    # fireList = []
    # for i in range(int(math.floor(float(len(BFSpathTarget)))/5)):
    #     # fireSet1 = m1.getSquaresOnFire()
    #     # fireList.append(fireSet1)
    #     freeSquares = msim.getFreeSquares()  # gets free squares after fire has been placed
    #     fireSet = msim.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
    #     # print("Fire Set: ", fireSet)
    #     msim.spreadFire(fireSet)  # spreads the fire

    # print(msim.map1)
    # BFSpathTarget2 = msim.bfs([(0, 0)], 3, m1.dim - 1, m1.dim - 1)
    # print(BFSpathTarget2)
    # print(m1.map1)
    s = (0,0)
    i =0
    while(True):
        BFSpathTarget2 = sim(len(BFSpathTarget), m1, qu, s)
        
        print(BFSpathTarget2)

        if BFSpathTarget2 == []:
            print("You're doomed")
            return 0
        s=BFSpathTarget2[len(BFSpathTarget2)-1]
        if BFSpathTarget2 != []:
            #you have to book it now
            fireList = []
            for i in range(len(BFSpathTarget2)):
                fireSet1 = m1.getSquaresOnFire()
                fireList.append(fireSet1)
                freeSquares = m1.getFreeSquares()  # gets free squares after fire has been placed
                fireSet = m1.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
                # print("Fire Set: ", fireSet)
                m1.spreadFire(fireSet)  # spreads the fire
            print(len(fireList))
            print(len(BFSpathTarget2))
            # print(fireList)
            flag1=False
            for i in range(len(fireList)):
                if BFSpathTarget2[i] in fireList[i]:
                    print("Fire Fire Fire Fire Fire")
                    print("The person burns at"+str(BFSpathTarget2[i]))
                    flag1=True
                    return 0

            if not flag1:
                print("He made it through")
                s = BFSpathTarget2[i]
                # return 1
            print("OK")

            if m1.map1[s[0]][s[1]] == 3:
                return 1
    
    # print(s)
    # BFSpathTarget2 = sim(len(BFSpathTarget), m1, qu, s)
    # print(BFSpathTarget2)
    
    # if BFSpathTarget2 == []:
    #     print("You're doomed")

    # else:
    #     #you have to book it now
    #     fireList = []
    #     for i in range(len(BFSpathTarget2)):
    #         fireSet1 = m1.getSquaresOnFire()
    #         fireList.append(fireSet1)
    #         freeSquares = m1.getFreeSquares()  # gets free squares after fire has been placed
    #         fireSet = m1.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
    #         # print("Fire Set: ", fireSet)
    #         m1.spreadFire(fireSet)  # spreads the fire
    #     print(len(fireList))
    #     print(len(BFSpathTarget2))
    #     # print(fireList)
    #     flag1=False
    #     for i in range(len(fireList)):
    #         if BFSpathTarget2[i] in fireList[i]:
    #             print("Fire Fire Fire Fire Fire")
    #             print("The person burns at"+str(BFSpathTarget2[i]))
    #             flag1=True
    #             return 0

    #     if not flag1:
    #         print("He made it through")
    #         s = BFSpathTarget2[i]
    #         # return 1
    #     print("OK")

    #     s=BFSpathTarget2[len(BFSpathTarget2)-1]
    # print(s)
    # BFSpathTarget2 = sim(len(BFSpathTarget), m1, qu, s)
    # print(BFSpathTarget2)
    
    # if BFSpathTarget2 == []:
    #     print("You're doomed")

    # else:
    #     #you have to book it now
    #     fireList = []
    #     for i in range(len(BFSpathTarget2)):
    #         fireSet1 = m1.getSquaresOnFire()
    #         fireList.append(fireSet1)
    #         freeSquares = m1.getFreeSquares()  # gets free squares after fire has been placed
    #         fireSet = m1.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
    #         # print("Fire Set: ", fireSet)
    #         m1.spreadFire(fireSet)  # spreads the fire
    #     print(len(fireList))
    #     print(len(BFSpathTarget2))
    #     # print(fireList)
    #     flag1=False
    #     for i in range(len(fireList)):
    #         if BFSpathTarget2[i] in fireList[i]:
    #             print("Fire Fire Fire Fire Fire")
    #             print("The person burns at"+str(BFSpathTarget2[i]))
    #             flag1=True
    #             return 0

    #     if not flag1:
    #         print("He made it through")
    #         s = BFSpathTarget2[i]
    #         # return 1
    #     print("OK")

    # s=BFSpathTarget2[len(BFSpathTarget2)-1]
    # print(s)
    # BFSpathTarget2 = sim(len(BFSpathTarget), m1, qu, s)
    # print(BFSpathTarget2)
    
    # if BFSpathTarget2 == []:
    #     print("You're doomed")

    # else:
    #     #you have to book it now
    #     fireList = []
    #     for i in range(len(BFSpathTarget2)):
    #         fireSet1 = m1.getSquaresOnFire()
    #         fireList.append(fireSet1)
    #         freeSquares = m1.getFreeSquares()  # gets free squares after fire has been placed
    #         fireSet = m1.getFireSet(qu, freeSquares)  # list of squares that will be set on fire after 1 turn
    #         # print("Fire Set: ", fireSet)
    #         m1.spreadFire(fireSet)  # spreads the fire
    #     print(len(fireList))
    #     print(len(BFSpathTarget2))
    #     # print(fireList)
    #     flag1=False
    #     for i in range(len(fireList)):
    #         if BFSpathTarget2[i] in fireList[i]:
    #             print("Fire Fire Fire Fire Fire")
    #             print("The person burns at"+str(BFSpathTarget2[i]))
    #             flag1=True
    #             return 0

    #     if not flag1:
    #         print("He made it through")
    #         s = BFSpathTarget2[i]
    #         # return 1
    #     print("OK")

    # print(len(fireList))
    # print(len(BFSpathTarget))

    # flag1=False
    # for i in range(len(fireList)):
    #     if BFSpathTarget[i] in fireList[i]:
    #         print("Fire Fire Fire Fire Fire")
    #         print("The person burns at"+str(BFSpathTarget[i]))
    #         flag1=True
    #         return 0

    # if not flag1:
    #     print("He made it through")
    #     return 1
print(test(0.2))