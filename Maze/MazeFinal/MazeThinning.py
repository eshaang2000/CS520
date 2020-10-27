import numpy as np
import random
from Node import Node
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

    def getAdjDiagonals(self, x, y):
        # get the adjacent indices
        # the possible movements are up, down, right, and left
        ans = []
        right = (x, y + 1)
        left = (x, y - 1)
        up = (x - 1, y)
        down = (x + 1, y)
        upRight = (x - 1, y + 1)
        upLeft = (x - 1, y - 1)
        downRight = (x + 1, y + 1)
        downLeft = (x + 1, y - 1)
        ans.append(right)
        ans.append(left)
        ans.append(up)
        ans.append(down)
        ans.append(upRight)
        ans.append(upLeft)
        ans.append(downRight)
        ans.append(downLeft)
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

    

    # get valid successors of a cell (valid unblocked cells)

    def getSuccessors(self, x, y):
        adj = []

        adj = self.getAdj(x, y) # get all adjacents

        # check if they are valid, if they are, retrieve them

        length = len(adj)

        valid = []

        for i in range(length):
            x_cord = adj[i][0]
            y_cord = adj[i][1]
            if self.legal(x_cord, y_cord):
                valid.append(adj[i])
                
            else:
                continue


        free = []
        

        # check if they are unblocked, if they are, retreive them

        length = len(valid)

        for i in range(length):
            x_cord = valid[i][0]
            y_cord = valid[i][1]
            if self.map1[x_cord][y_cord] == 0:
                continue
            else:
                free.append(valid[i])  

        return free

        
        


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

    # gets a list of blocked squares on the map (squares with value of 0)

    def getBlockedSquares(self):
        ans = []
        for x in range(0, self.dim):
            for y in range(0, self.dim):
                if self.map1[x][y] == 0:
                    cord = (x, y)
                    ans.append(cord)
        return ans

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

    def bfsDiagonal(self, queue, target, targetx,
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
            adjs = self.getAdjDiagonals(fringe[0], fringe[1])

            #if self.map1[fringe[0]][fringe[1]] == 2:
                #print("Our attempt has started")

            if self.map1[fringe[0]][fringe[1]] == target:
                #print("Goal reached")
                #print("This is how you go about it")
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
            #print("No way to goal")
            return []
        return path

    def thinMaze(self, p): # method to thin maze, will remove a fraction p of the maze's obstacles at random
        blockedSquares = self.getBlockedSquares()
        size = len(blockedSquares)
        numberOfBlocksToChange = round(p*size)
        change_list = random.sample(blockedSquares, numberOfBlocksToChange)
        for i in range(len(change_list)):
            x_cord = change_list[i][0]
            y_cord = change_list[i][1]
            self.map1[x_cord][y_cord] = 1

    def manhattanDistance(self, curr_x, curr_y, goal_x, goal_y):
        h = abs(curr_x - goal_x) + abs(curr_y - goal_y)
        return h

    def getShortestPathLengths(self, goal_x, goal_y):
        h_values = np.zeros((self.dim, self.dim))
        goal = (goal_x, goal_y)
        for row in range(self.dim):
            for col in range(self.dim):
                if self.map1[row][col] == 0:
                    continue
                else:
                    current = (row, col)
                    path = self.aStarManhattan(current, goal)
                    length = len(path)
                    h_values[row][col] = length

        return h_values

    def getShortestPathLength(self, current_x, current_y, goal_x, goal_y):
        goal = (goal_x, goal_y)
        current = (current_x, current_y)
        path = self.aStarManhattan(current, goal)
        length = len(path)
        return length

    def getDiagonalPathLengths(self, current_x, current_y, goal_x, goal_y):
        goal = (goal_x, goal_y)
        current = (current_x, current_y)
        path = self.bfsDiagonal([current], 3, self.dim - 1, self.dim - 1)
        length = len(path)
        return length
        

    """ 
    Citation for idea:
    Looked at - not copied from geeksforgeeks.com  and medium.com. Can reproduce if asked.  """
    def aStarManhattan(self, start, finish): # A* algorithm to solve thinned maze via Manhattan Distance
        count = 0 
        open_list = [] # list of open nodes to explore
        closed_list = [] # list of closed nodes
        positions_visited = []

        path = [] # path to return once we find goal

        # add start node
        start_node = Node(None, start)

        goal_x = finish[0]
        goal_y = finish[1]

        open_list.append(start_node)

        foundEnd = False


        # while open list is not empty
        while len(open_list) != 0:

            index = 0
            q = open_list[0]
            smallestF = open_list[0].f
            
            # get node with smallest f
            for i in range(len(open_list)):
                if open_list[i].f < smallestF:
                    q = open_list[i]
                    index = i                    
                    smallestF = open_list[i].f
            
            q = open_list.pop(index) # pop smallest f node off list to explore
            closed_list.append(q) # add that node to closed list


            q_x_cord = q.position[0]
            q_y_cord = q.position[1]


            if q_x_cord == goal_x and q_y_cord == goal_y: # if node is goal node, we are done. get path
                ptr_node = q
                while ptr_node is not None:
                    path.append(ptr_node.position)
                    ptr_node = ptr_node.parent
                path.reverse()
                foundEnd = True
                break

            successors = self.getSuccessors(q_x_cord, q_y_cord) # get valid, unblocked successors

            for i in range(len(successors)):
                s = successors[i]
                new_x_cord = s[0]
                new_y_cord = s[1]
                curr_node = Node(q, (new_x_cord, new_y_cord))

                inClosedList = False

                for j in closed_list:
                    if curr_node.position == j.position: # do not add
                        inClosedList = True
                        break

                if inClosedList == True:
                    continue

                #so you check if you have visited new_x_cord new_y_cord
                if curr_node.position in positions_visited:
                    continue

                curr_node.g = q.g + 1
                curr_node.h = self.manhattanDistance(new_x_cord, new_y_cord, goal_x, goal_y)
                # print(str(new_x_cord) +" "+ str(new_y_cord))
                count+=1
                curr_node.f = curr_node.g + curr_node.h

                positions_visited.append(curr_node.position)



                doNotAdd = False

                for j in open_list:
                    if curr_node.position == j.position:
                        if curr_node.g > j.g: # do not add
                            doNotAdd = True
                            break

                if doNotAdd == True:
                    continue

                open_list.append(curr_node)


        if foundEnd == True:
            return path
        else:
            return []

    def aStarMH(self, start, finish): # A* algorithm to solve thinned maze via Manhattan Distance but returns number of visited nodes instead of other one
        count = 0 
        open_list = [] # list of open nodes to explore
        closed_list = [] # list of closed nodes
        positions_visited = []

        path = [] # path to return once we find goal

        # add start node
        start_node = Node(None, start)

        goal_x = finish[0]
        goal_y = finish[1]

        open_list.append(start_node)

        foundEnd = False


        # while open list is not empty
        while len(open_list) != 0:

            index = 0
            q = open_list[0]
            smallestF = open_list[0].f
            
            # get node with smallest f
            for i in range(len(open_list)):
                if open_list[i].f < smallestF:
                    q = open_list[i]
                    index = i                    
                    smallestF = open_list[i].f
            
            q = open_list.pop(index) # pop smallest f node off list to explore
            closed_list.append(q) # add that node to closed list


            q_x_cord = q.position[0]
            q_y_cord = q.position[1]


            if q_x_cord == goal_x and q_y_cord == goal_y: # if node is goal node, we are done. get path
                ptr_node = q
                while ptr_node is not None:
                    path.append(ptr_node.position)
                    ptr_node = ptr_node.parent
                path.reverse()
                foundEnd = True
                break

            successors = self.getSuccessors(q_x_cord, q_y_cord) # get valid, unblocked successors

            for i in range(len(successors)):
                s = successors[i]
                new_x_cord = s[0]
                new_y_cord = s[1]
                curr_node = Node(q, (new_x_cord, new_y_cord))

                inClosedList = False

                for j in closed_list:
                    if curr_node.position == j.position: # do not add
                        inClosedList = True
                        break

                if inClosedList == True:
                    continue

                #so you check if you have visited new_x_cord new_y_cord
                if curr_node.position in positions_visited:
                    continue

                curr_node.g = q.g + 1
                curr_node.h = self.manhattanDistance(new_x_cord, new_y_cord, goal_x, goal_y)
                # print(str(new_x_cord) +" "+ str(new_y_cord))
                count+=1
                curr_node.f = curr_node.g + curr_node.h

                positions_visited.append(curr_node.position)



                doNotAdd = False

                for j in open_list:
                    if curr_node.position == j.position:
                        if curr_node.g > j.g: # do not add
                            doNotAdd = True
                            break

                if doNotAdd == True:
                    continue

                open_list.append(curr_node)


        if foundEnd == True:
            return count
        else:
            return -1

    def getThinMazeHeuristics(self, x, y, shortestPathLengths):
        h = shortestPathLengths[x][y]
        return h

    def getDiagonalHeuristics(self, x, y, diagonalPathLengths):
        h = diagonalPathLengths[x][y]
        return h

    
    def aStarBootStrapped(self, start, finish, map): # A* algorithm to solve thinned maze via Manhattan Distance

        open_list = [] # list of open nodes to explore
        closed_list = [] # list of closed nodes
        positions_visited = []

        path = [] # path to return once we find goal

        # add start node
        start_node = Node(None, start)

        goal_x = finish[0]
        goal_y = finish[1]

        open_list.append(start_node)

        foundEnd = False

        count = 0

        # while open list is not empty
        while len(open_list) != 0:

            index = 0
            q = open_list[0]
            smallestF = open_list[0].f
            
            # get node with smallest f
            for i in range(len(open_list)):
                if open_list[i].f < smallestF:
                    q = open_list[i]
                    index = i                    
                    smallestF = open_list[i].f
            
            q = open_list.pop(index) # pop smallest f node off list to explore
            closed_list.append(q) # add that node to closed list

            q_x_cord = q.position[0]
            q_y_cord = q.position[1]


            if q_x_cord == goal_x and q_y_cord == goal_y: # if node is goal node, we are done. get path
                ptr_node = q
                while ptr_node is not None:
                    path.append(ptr_node.position)
                    ptr_node = ptr_node.parent
                path.reverse()
                foundEnd = True
                break

            successors = self.getSuccessors(q_x_cord, q_y_cord) # get valid, unblocked successors

            for i in range(len(successors)):
                s = successors[i]
                new_x_cord = s[0]
                new_y_cord = s[1]
                curr_node = Node(q, (new_x_cord, new_y_cord))

                inClosedList = False

                for j in closed_list:
                    if curr_node.position == j.position: # do not add
                        inClosedList = True
                        break

                if inClosedList == True:
                    continue

                if curr_node.position in positions_visited:
                    continue

                curr_node.g = q.g + 1
                curr_node.h = map.getShortestPathLength(new_x_cord, new_y_cord, goal_x, goal_y)
                count += 1
                curr_node.f = curr_node.g + curr_node.h

                positions_visited.append(curr_node.position)



                doNotAdd = False

                for j in open_list:
                    if curr_node.position == j.position:
                        if curr_node.g > j.g: # do not add
                            doNotAdd = True
                            break

                if doNotAdd == True:
                    continue

                open_list.append(curr_node)


        if foundEnd == True:
            return count
        else:
            # print("No way to end")
            return -1

    def aStarDiagonal(self, start, finish): # A* algorithm to solve original maze using Diagonal Path Lengths as Heuristics

        open_list = [] # list of open nodes to explore
        closed_list = [] # list of closed nodes
        positions_visited = []

        path = [] # path to return once we find goal

        # add start node
        start_node = Node(None, start)

        goal_x = finish[0]
        goal_y = finish[1]

        open_list.append(start_node)

        foundEnd = False
        count = 0


        # while open list is not empty
        while len(open_list) != 0:

            index = 0
            q = open_list[0]
            smallestF = open_list[0].f
            
            # get node with smallest f
            for i in range(len(open_list)):
                if open_list[i].f < smallestF:
                    q = open_list[i]
                    index = i                    
                    smallestF = open_list[i].f
            
            q = open_list.pop(index) # pop smallest f node off list to explore
            closed_list.append(q) # add that node to closed list

            q_x_cord = q.position[0]
            q_y_cord = q.position[1]


            if q_x_cord == goal_x and q_y_cord == goal_y: # if node is goal node, we are done. get path
                ptr_node = q
                while ptr_node is not None:
                    path.append(ptr_node.position)
                    ptr_node = ptr_node.parent
                path.reverse()
                foundEnd = True
                break

            successors = self.getSuccessors(q_x_cord, q_y_cord) # get valid, unblocked successors

            for i in range(len(successors)):
                s = successors[i]
                new_x_cord = s[0]
                new_y_cord = s[1]
                curr_node = Node(q, (new_x_cord, new_y_cord))

                inClosedList = False

                for j in closed_list:
                    if curr_node.position == j.position: # do not add
                        inClosedList = True
                        break

                if inClosedList == True:
                    continue


                if curr_node.position in positions_visited:
                    continue

                
                curr_node.g = q.g + 1
                curr_node.h = self.getDiagonalPathLengths(new_x_cord, new_y_cord, goal_x, goal_y)
                count += 1
                positions_visited.append(curr_node.position)
                curr_node.f = curr_node.g + curr_node.h



                doNotAdd = False

                for j in open_list:
                    if curr_node.position == j.position:
                        if curr_node.g > j.g: # do not add
                            doNotAdd = True
                            break

                if doNotAdd == True:
                    continue

                open_list.append(curr_node)


        if foundEnd == True:
            return count
        else:
            # print("No way to end")
            return -1

def test(p):
    fail = (-1, -1)
    m1 = Map(10)  # dimensions
    print("Original Maze")
    m1.populate(0.3)  # populates using parameter prob
    print("A* Manhattan Path for regular maze")
    manhattanNodes = m1.aStarMH( (0, 0), (m1.dim - 1, m1.dim - 1) )
    print(manhattanNodes)

    if manhattanNodes == -1:
        return fail

    m2 = copy.deepcopy(m1) # make copy of maze to thin
    m2.thinMaze(p)
    #print(m2.map1)
    thinNodes= m1.aStarBootStrapped( (0,0), (m1.dim - 1, m1.dim - 1), m2)
    print("A* path for regular maze using shortest path lengths heuristics")
    print(thinNodes)

    
    
    compare = (manhattanNodes, thinNodes)
    return compare

def test2(p):
    fail = (-1, -1)
    m1 = Map(10)
    print("Original Maze")
    m1.populate(0.3) # populates using parameter prob
    print("A* Manhattan Path for regular maze")
    manhattanNodes = m1.aStarMH( (0, 0), (m1.dim - 1, m1.dim - 1) )
    print(manhattanNodes)

    if manhattanNodes == -1:
        return fail

    m2 = copy.deepcopy(m1)
    m2.thinMaze(p)
    thinNodes = m1.aStarDiagonal( (0,0), (m1.dim - 1, m1.dim - 1) )
    print("A* path for regular maze using diagonal heuristics")
    print(thinNodes)

    compare = (manhattanNodes, thinNodes)
    return compare    

    






    
