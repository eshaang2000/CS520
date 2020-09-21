import numpy as np
import random
import pygame


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

    def trace(self, traceSet):
        final = (self.dim - 1, self.dim - 1)
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

    def savePath(self, stack):
        path = []
        for i in range(len(stack)):
            x = stack.pop()
            path.append(x)
            print(x)
        return path

    def bfs(self, queue):

        # map1 = np.zeros((self.dim, self.dim))
        # map1[0][0]=(2,3)
        # print(map1)
        # queue = [(0, 0)] # you start with
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
        # print("woah")
        traceSet = {(0, 0): None}
        # print(traceSet.get((0,0)))
        flag = False #variable to see if it is possible to reach the goal
        while queue:
            fringe = queue.pop(0)  ##gets 0, 0 first
            adjs = self.getAdj(fringe[0], fringe[1])

            if self.map1[fringe[0]][fringe[1]] == 2:
                print("Our attempt has started")

            if self.map1[fringe[0]][fringe[1]] == 3:
                print("Goal reached")
                print("This is how you go about it")
                ans = self.trace(traceSet)
                path = self.savePath(ans)
                flag = True
                # print(ans.pop())
                break

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
                    # print(adjs[i])
                    traceSet[adjs[i]] = fringe
                    queue.append(adjs[i])
        if flag is False:
            print("No way to goal")
            return []
        # print(traceSet)
        return path



m1 = Map(10)  # dimensions
m1.populate(0.3)  # populTES Usind parameter prob
BFSpath = m1.bfs([(0, 0)])
# print(BFSpath)

# Programming the Maze GUI

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 100, 10)
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20
 
# This sets the margin between each cell
MARGIN = 5

x = m1.dim # want the Maze GUI to have same dimensions as Map Object
 
#Create Maze 2-D Array
grid = []
for row in range(int(x)):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(int(x)):
        grid[row].append(0)  # Append a cell
 
# Initialize pygame
pygame.init()

 
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [600, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Array Backed Grid")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop 
    # Set the screen background
    screen.fill(GREEN)
    # Draw the grid
    for row in range(int(x)):
        for column in range(int(x)):
            color = WHITE # white indicates free cell
            if m1.map1[row][column] == 0:
                color = BLACK # black indicates occupied cell
            block = (row, column)
            # print(block)
            if block in BFSpath:
                color = BLUE # blue indicates BFS path
            if m1.map1[row][column] == 2:
                color = YELLOW # yellow indicates start
            if m1.map1[row][column] == 3:
                color = ORANGE # orange indicates finish
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
    
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Update screen
    pygame.display.flip()
 
pygame.quit()