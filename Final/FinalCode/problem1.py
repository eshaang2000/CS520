import numpy as np
import sys

print(sys.getrecursionlimit())


# sys.setrecursionlimit(10500)
def legal(s):
    if s[0] < 0 or s[0] >= 7:
        return False
    if s[1] < 0 or s[1] >= 7:
        return False
    return True


def getAdj(s):
    lista = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    ans = []
    for i in lista:
        ans.append((s[0] + i[0], s[1] + i[1]))
    return ans


def trace(traceSet, x, y):
    final = (x, y)
    stack = [final]
    back = traceSet[final]

    while back is not None:
        stack.append(back)
        back = traceSet[back]
        # print(back)
    return stack


def bfs(s, d, start, finish):
    """
    1. makes the board with the imputs given in terms of 1 dog and 1 sheep start, and finish
    :return: idk yet
    """
    # print("the s")
    # print(s)
    if not legal(s):
        # print("The illegal s")
        # print(s)
        return 0, start
    if start == finish:
        return 0, start
    grid = np.zeros((7, 7))
    grid[s[0]][s[1]] = 2
    grid[d[0]][d[1]] = 2  # the second dog so that they don't come onto the same position
    grid[finish[0]][finish[1]] = 7
    thisset = {start}
    traceSet = {start: None}
    queue = [start]
    flag = False  # variable to see if it is possible to reach the goal
    while queue:  # gets 0, 0 first
        fringe = queue.pop(0)
        adjs = getAdj(fringe)
        if grid[fringe[0]][fringe[1]] == 7:
            ans = trace(traceSet, finish[0], finish[1])
            return len(ans), ans[len(ans) - 2]
        if grid[fringe[0]][fringe[1]] == 2:
            continue
        for i in range(len(adjs)):
            if legal(adjs[i]):
                if adjs[i] in thisset:
                    continue
                thisset.add(adjs[i])
                traceSet[adjs[i]] = fringe  # adjs i comes from fringe
                queue.append(adjs[i])

    if flag is False:
        print("No way to goal")
        return (0, start)
    # return path

def Tc(d1, d2, s):
    grid = np.zeros((7, 7))
    grid[s[0]][s[1]] = 2
    grid[d1[0]][d1[1]] = 1
    grid[d2[0]][d2[1]] = 1
    print(grid)
    if legal((s[0], s[1]-1)) and legal((s[0]-1, s[1])):
        l1, m1 = bfs(s, d2, d1, (s[0] - 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] - 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] - 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] - 1))
        if l1 <= l3:
            f1 = l1
            f2 = l4
        else:
            f1 = l2
            f2 = l3
        print(f1)
        print(f2)
        a = max(f1, f2)
        return a + 12 - s[0] - s[1]
    elif legal((s[0]+1, s[1])) and legal((s[0], s[1]-1)):
        l1, m1 = bfs(s, d2, d1, (s[0] +1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] + 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] - 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] - 1))
        if l1 <= l3:
            f1 = l1
            f2 = l4
        else:
            f1 = l2
            f2 = l3
        a = max(f1, f2)
        return a + 12-s[1]
    elif legal((s[0]-1, s[1])) and legal((s[0], s[1]+1)):
        l1, m1 = bfs(s, d2, d1, (s[0] - 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] - 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] + 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] + 1))
        if l1 <= l3:
            f1 = l1
            f2 = l4
        else:
            f1 = l2
            f2 = l3
        print(f1)
        print(f2)
        a = max(f1, f2)
        return a + 12 - s[0]
    elif legal((s[0], s[1]+1)) and legal((s[0]+1, s[1])):
        l1, m1 = bfs(s, d2, d1, (s[0] + 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] + 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] + 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] + 1))
        if l1 <= l3:
            f1 = l1
            f2 = l4
        else:
            f1 = l2
            f2 = l3
        print(f1)
        print(f2)
        a = max(f1, f2)
        return a + 12

print(Tc((0, 6), (6, 3), (4, 0)))


def T(d1, d2, s):
    # print(legal(s))
    # print(d1)
    # print(d2)
    # print(s)
    if not legal(s) or d1 == s or d2 == s:
        # print("this")
        return 0
    # input()
    grid = np.zeros((7, 7))
    grid[s[0]][s[1]] = 2
    grid[d1[0]][d1[1]] = 1
    grid[d2[0]][d2[1]] = 1
    print(grid)
    if (d1 == (s[0] - 1, s[1]) and d2 == (s[0], s[1] - 1)) or (d1 == (s[0], s[1] - 1) and d2 == (s[0] - 1, s[1])):
        print("A case")
        return 12 - s[0] - s[1]  # great base case
    if (d1 == (s[0] + 1, s[1]) and d2 == (s[0], s[1] + 1)) or (d1 == (s[0], s[1] + 1) and d2 == (s[0] + 1, s[1])):
        print("B case")
        return 13 + s[0] + s[1]
    if (d1 == (s[0] - 1, s[1]) and d2 == (s[0], s[1] + 1)) or (d1 == (s[0], s[1] + 1) and d2 == (s[0] - 1, s[1])):
        print("C case")
        return 7 + s[1]
    if (d1 == (s[0] + 1, s[1]) and d2 == (s[0], s[1] - 1)) or (d1 == (s[0], s[1] - 1) and d2 == (s[0] + 1, s[1])):
        print("D case")
        return 7 + s[0]
    l1 = 0
    l2 = 0
    l3 = 0
    l4 = 0
    m1 = 0
    m2 = 0
    m3 = 0
    m4 = 0
    if legal((s[0] - 1, s[1])) and legal((s[0], s[1] - 1)):
        print("A")
        l1, m1 = bfs(s, d2, d1, (s[0] - 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] - 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] - 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] - 1))

    elif legal((s[0] - 1, s[1])) and legal((s[0], s[1] + 1)):
        print("B")
        l1, m1 = bfs(s, d2, d1, (s[0] - 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] - 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] + 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] + 1))
        # print(l1, l2, l3, l4)

    elif legal((s[0] - 1, s[1])) and legal((s[0], s[1] - 1)):
        print("C")
        l1, m1 = bfs(s, d2, d1, (s[0] - 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] - 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] - 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] - 1))

    elif legal((s[0] + 1, s[1])) and legal((s[0], s[1] + 1)):
        print("D")
        l1, m1 = bfs(s, d2, d1, (s[0] + 1, s[1]))
        l3, m3 = bfs(s, d1, d2, (s[0] + 1, s[1]))
        l4, m4 = bfs(s, d1, d2, (s[0], s[1] + 1))
        l2, m2 = bfs(s, d2, d1, (s[0], s[1] + 1))
    f1 = 0
    f2 = 0
    # if this is cnahnged the sequence they run in changes so yeah
    if l1 <= l3:
        f1 = m1
        f2 = m4
    else:
        f1 = m2
        f2 = m3
    # now we will experiment with the sheep moving
    poMoves = [[1, 0], [0, 1]]
    adj = []
    da = 0
    print(f1, f2)
    # return 1 + T(f1, f2, (s[0] - 1, s[1])) + T(f1, f2, (s[0], s[1] - 1))
    return 1+ T(f1, f2, (s[0]+1, s[1]))+T(f1, f2, (s[0], s[1]+1))+T(f1, f2, (s[0], s[1]-1))+T(f1, f2, (s[0]-1, s[1]))
    # da += 1 + T(f1, f2, (s[0] + 1, s[1]))
    # return da
    # for i in poMoves:
    #     temp = (s[0]+i[0], s[1]+i[1])
    #     if not legal(temp) or temp == f1 or temp == f2:
    #         continue
    #     adj.append(temp)
    # if len(adj) == 0:
    #     return 1+T(f1, f2, s)
    # for i in adj:
    #     return 1+T(f1, f2, i)
    # print(da)


# print(T((0, 2), (2, 0), (1, 0)))
