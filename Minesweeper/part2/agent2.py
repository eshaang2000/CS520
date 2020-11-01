import environment
import numpy as np
import random
score = 0
n = 10
m = 8
hiddenBoard = np.asfarray(environment.makeBoard(n, m))
board = np.zeros((n, n))
board.fill(-10)
known_safe = set()
known_mine = set()
explored = set()#to mark the stuff that has already been minenatored or safenatored
knowledge_base = []
#so this is good
def mark_mine(x, y):
    if(x<0 or y<0):
        return
    if(x>=n or y>=n):
        return
    # remove_knowledge(x, y)
    known_mine.add((x, y))

#so this is good too
def mark_safe(x, y):
    if(x<0 or y<0):
        return
    if(x>=n or y>=n):
        return
    # remove_knowledge(x, y)
    known_safe.add((x, y))

def remove_knowledge(x, y):
    rem = (x, y)
    for i in knowledge_base:
        for j in i:
            # print(i[j])
            if (x,y) in i[j]:
                i[j].remove((x, y))

# Adds an array of tuples to point to query number
# works
def add_knowledge(query,arr):
    removal = []
    for i in arr:
        # print("poop")
        # print(i)
        if(i[0]<0 or i[1]<0):
            removal.append(i)
        if(i[0]>=n or i[1]>=n):
            removal.append(i)
        if(i in known_mine):
            query-=1
            removal.append(i)
        if(i in known_safe):
            removal.append(i)
    # knowledge_base[arr] 
    # print(removal)
    for i in removal:
        # print("something removed")
        if i in arr:
            arr.remove(i)
    # print("The array is")
    # print(arr)
    if {query:arr} in knowledge_base:
        return
    knowledge_base.append({query:arr})

# Fills up the knowledge base
# this works
def afterQuery():
    for i in range(n):
        for j in range(n):
            if board[i][j]!=-10 and board[i][j]!=-1 and board[i][j]!=-7:
                # I want to add all the surroundings to my knowledge base. Will think about complications later
                arr = [(i-1, j),(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
                query = board[i][j]
                add_knowledge(query, arr)

def randomGuess():
    # k = random.randint(0, n-1)
    # l = random.randint(0, n-1)
    # while (k,l) in known_safe or (k,l) in known_mine:
    #     k = random.randint(0, n-1)
    #     l = random.randint(0, n-1)
    rando = []
    for i in range(n):
        for j in range(n):
            if board[i][j]==-10:
                rando.append((i, j))
    ans = random.choice(rando)
    return ans

def makeRandomGuess():
    a = randomGuess()
    query(a[0], a[1])
    if board[a[0]][a[1]] == -1:
        print("unlucky")
        # score+=1
    explored.add((a[0], a[1]))

def query(x, y):
    global score
    board[x][y] = environment.query(x, y, hiddenBoard)
    if board[x][y] == -1:
        score+=1
        known_mine.add((x, y))

#We have identified a mine there
def flag(x, y):
    board[x][y] = -7
#i[j] is tha array
#iterates through the whole array and find out mines in the knowledge base
def minenator():
    flag1 = False
    removal = []
    for i in knowledge_base:
        for j in i:
            if j ==0 :
                continue
            if len(i[j]) == j:
                flag1 = True
                for k in i[j]:
                    mark_mine(k[0], k[1])
                    flag(k[0], k[1])
                    explored.add((k[0], k[1]))
                    afterQuery()
                removal.append(i)
    for i in removal:
        knowledge_base.remove(i)
    # print(known_mine)    
    return flag1
                # print("wor") # we have to do something for the knowledge pass - just mark everything as mines 

        # print(knowledge_base[i])

def safenator():
    flag1 = False
    removal = []
    for i in knowledge_base:
        for j in i:
            if 0 == j:
                # print(i)
                removal.append(i)
                if len(i[j]) == 0:
                    continue
                flag1 = True
                for k in i[j]:
                    # remove_knowledge(k[0], k[1])
                    mark_safe(k[0], k[1])
                    query(k[0], k[1])
                    explored.add((k[0], k[1]))
                    afterQuery()
    for i in removal:
        knowledge_base.remove(i)
    # print(known_safe) 
    return flag1

""" 
1. I want to check the whole knowledge base to see if there are any subsets present
2. if there are then lets see """
def setanator():
    flag1 = False
    count = []
    arrs = []
    removal = []
    for i in knowledge_base:
        for j in knowledge_base:
            if i==j:
                continue
            set1 = set()
            set2 = set()
            count1 = 0
            count2 = 0
            count3 = 0
            if(isSubset(listGetter(i), listGetter(j))): #i is a subset of j
                removal.append(j)
                flag1 = True
                set1 = set(listGetter(i))
                set2 = set(listGetter(j))
                set3 = set2.difference(set1)
                count3 = queryGetter(j) - queryGetter(i)
                # print(set3)
                # print(count3)
                count.append(count3)
                arrs.append(list(set3))
    # print(count)
    # print(arrs)

    for i in range(len(count)):
        # print(arrs[i])
        add_knowledge(count[i], arrs[i])
    # for i in removal:
    #     knowledge_base.remove(i)
    return flag1


def listGetter(S):
    for i in S:
        return S[i]

def queryGetter(S):
    for i in S:
        return i

def isSubset(arr1, arr2): # arr1 is a subset of arr2
    if(set(arr1).issubset(set(arr2))): 
        return True
    return False

def fin():
    for i in range(n):
        for j in range(n):
            if board[i][j]==-10:
                return False
    return True


def test(n1, m1):
    global score
    global n
    global m
    global hiddenBoard
    global board
    global known_safe
    global known_mine
    global explored
    global knowledge_base
    n = n1
    m = m1
    hiddenBoard = np.asfarray(environment.makeBoard(n, m))
    board = np.zeros((n, n))
    board.fill(-10)
    known_safe = set()
    known_mine = set()
    explored = set()#to mark the stuff that has already been minenatored or safenatored
    knowledge_base = []
    print(hiddenBoard)
    makeRandomGuess()
    afterQuery()

    while(not fin()):
        flag1 = False
            # input("Press Enter to continue...")
            # print("setanator")
        # setanator()
            # print("safenator")
        flag2= safenator()
        flag1 = flag1 or flag2
            # print(flag1)
            # print("minenator")
        flag3 = minenator()
        flag1 = flag1 or flag3
        q = knowledge_base
        afterQuery()
        if fin():
            # print(knowledge_base)
            print("the score is")
            print(board)
            sc = m
            for i in range(n):
                for j in range(n):
                    if board[i][j] == -1:
                        sc-=1
            print((sc)/m)
            return((sc)/m)
            break
            # print(flag1)
        if flag1 == False:
                # print("making a random guess")
            makeRandomGuess()
            # print(knowledge_base)
            # print(board)
            # print(score)
    # test(8, 10)
for i in range(100):
    if test(8, 10) == None:
        print("danger")
