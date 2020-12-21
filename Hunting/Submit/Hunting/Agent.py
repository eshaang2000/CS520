import numpy as np
import random

from Landscape import Landscape


class Agent:
    def __init__(self, dim):
        self.map1 = np.zeros((dim, dim))
        self.map2 = np.zeros((dim, dim))
        self.map3 = np.zeros((dim, dim))
        self.dim = dim
        prob = 1 / dim / dim
        self.land = Landscape(dim)
        for i in range(dim):
            for j in range(dim):
                self.map1[i][j] = prob
                self.map2[i][j] = prob
                self.map3[i][j] = prob

    def reset(self):
        self.land.setNewTarget()
        dim1 = self.dim
        self.map1 = np.zeros((dim1, dim1))
        self.map2 = np.zeros((dim1, dim1))
        self.map3 = np.zeros((dim1, dim1))
        self.dim = dim1
        prob = 1 / dim1 / dim1
        self.land = Landscape(dim1)
        for i in range(dim1):
            for j in range(dim1):
                self.map1[i][j] = prob
                self.map2[i][j] = prob
                self.map3[i][j] = prob

    def findMax(self, maps):
        maxNo = -10
        maxSet = set()
        for i in range(self.dim):
            for j in range(self.dim):
                if maps[i][j] == maxNo:
                    maxSet.add((i, j))
                if maps[i][j] > maxNo:
                    maxNo = maps[i][j]
                    maxSet = set()
                    maxSet.add((i, j))
        maxTu = random.choice(list(maxSet))
        return maxTu

    def findMin(self, maps, pos):
        maxNo = 1000000000000000000
        maxSet = set()
        for i in range(self.dim):
            for j in range(self.dim):
                if i == pos[0] and j == pos[1]:
                    continue
                if maps[i][j] == maxNo:
                    maxSet.add((i, j))
                if maps[i][j] < maxNo:
                    maxNo = maps[i][j]
                    maxSet = set()
                    maxSet.add((i, j))

        maxTu = random.choice(list(maxSet))
        return maxTu

    def normalize(self):
        sum1 = np.sum(self.map1)
        sum2 = np.sum(self.map2)
        for i in range(self.dim):
            for j in range(self.dim):
                self.map1[i][j] /= sum1
                self.map2[i][j] /= sum2

    def printMap(self):
        print(self.map1)

    def query(self, x, y):
        return self.land.query(x, y)

    def queryTerrain(self, x, y):
        return self.land.queryTerrainType(x, y)

    # Gets the probability of failure implications. Basically gets the probability of failure
    def getObservationProb(self, x, y):
        p1 = 1 - self.map1[x][y]
        p2 = self.map1[x][y] * self.land.queryTerrainType(x, y)
        # print(self.land.queryTerrainType(x, y))
        return p1 + p2

    def updateSelf(self, x, y):
        p = self.map1[x][y] * self.land.queryTerrainType(x, y)
        self.map1[x][y] = p / self.getObservationProb(x, y)
        self.updateOthers(x, y)
        # self.normalize()

    def updateOthers(self, x, y):
        for i in range(self.dim):
            for j in range(self.dim):
                if i == x and j == y:
                    continue
                self.map1[i][j] = self.map1[i][j] / self.getObservationProb(x, y)
        self.updateMap2()

    def updateMap2(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.map2[i][j] = self.map1[i][j] * (1 - self.queryTerrain(i, j))

    def updateMap3(self, pos):
        for i in range(self.dim):
            for j in range(self.dim):
                # if self.map1[i][j] <= 0.0001:
                #     continue
                if pos == (i, j):
                    continue
                self.map3[i][j] = manhattan((i, j), pos) / self.map1[i][j]
                # self.map3[i][j] = 1/self.map1[i][j]
                if self.map3[i][j] == 0:
                    print("Help")
                    print(manhattan((i, j), pos))
                    print(self.map1[i][j])
        # self.updateMap2(x, y)
        # self.map2[i][j] = self.map2[i][j] * self.queryTerrain(i, j)

    def queryMax(self):
        qo = self.findMax(self.map1)
        anso = self.land.query(qo[0], qo[1])
        return anso, qo

    def queryMax1(self):
        qo = self.findMax(self.map2)
        anso = self.land.query(qo[0], qo[1])
        return anso, qo

    def queryMax2(self, pos):
        qo = self.findMin(self.map3, pos)
        # print(qo)
        anso = self.land.query(qo[0], qo[1])
        return anso, qo


def manhattan(q, pos):
    return abs(pos[0] - q[0]) + abs(pos[1] - q[1])


def testRule1(aObj):
    itera = 0
    aObj.land.printTarget()
    type = 0
    while itera < 5000:
        # print(aObj.map1)
        # input()
        ans, q = aObj.queryMax()
        # print(itera)
        if ans:
            print("The target is at " + str(q))
            type = a.land.queryTerrain(q[0], q[1])
            break
        aObj.updateSelf(q[0], q[1])
        itera += 1
    if itera == 3000:
        return 0, 0
    return itera, type


def testRule2(aObj):
    itera = 0
    aObj.land.printTarget()
    type = 0
    while itera < 5000:
        # print(aObj.map1)
        # input()
        ans, q = aObj.queryMax1()
        if ans:
            print("The target is at " + str(q))
            type = aObj.land.queryTerrain(q[0], q[1])
            break
        aObj.updateSelf(q[0], q[1])
        itera += 1

    return itera, type


def basicAgent1(aObj, pos):
    itera = 0
    score1 = 0
    aObj.land.printTarget()
    type2 = 0
    while itera < 5000:
        ans, q = aObj.queryMax()
        score1 += abs(pos[0] - q[0]) + abs(pos[1] - q[1])
        pos = q
        if ans:
            print("The target is at " + str(q))
            type2 = aObj.land.queryTerrain(q[0], q[1])
            break
        aObj.updateSelf(q[0], q[1])
        itera += 1
        score1 += 1
    print("The score is ", end="")
    print(score1)
    if itera == 5000:
        return 0, 0
    return score1, type2


def basicAgent2(aObj, pos):
    itera = 0
    score = 0
    aObj.land.printTarget()
    while itera < 10000:
        ans, q = aObj.queryMax1()
        score += manhattan(pos, q)
        pos = q
        if ans:
            print("The target is at " + str(q))
            break
        aObj.updateSelf(q[0], q[1])
        itera += 1
        score += 1
    print("The score is ", end="")
    print(score)
    return itera


def basicAgent3(aObj, pos):
    itera = 0
    score = 0
    type2 = 0
    aObj.land.printTarget()
    while itera < 10000:
        # input()
        # print(aObj.map3)
        ans, q = aObj.queryMax2(pos)
        score += manhattan(pos, q)
        pos = q
        if ans:
            print("The target is at " + str(q))
            type2 = aObj.land.queryTerrain(q[0], q[1])
            break
        aObj.updateSelf(q[0], q[1])
        aObj.updateMap3(pos)
        itera += 1
        score += 1
    print("The score is ", end="")
    print(score)
    return score, type2


# a = Agent(20)
# print(testRule1(a))
# print(testRule2(a))
# print(basicAgent3(a, (0, 0)))

ans = []
nums = 0
a = Agent(25)
while nums < 100:
    a.reset()
    score, type1 = basicAgent3(a, (0, 0))
    nums += 1
    ans.append((type1, score))

print(ans)

# [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (1, 1922), (4, 2634), (2, 1265), (2, 1925), (3, 664), (0, 0), (2, 249),
# (1, 2335), (3, 737), (0, 0), (1, 527), (0, 0), (0, 0), (1, 483), (3, 2156)]

# Test1
# [(3, 2392), (3, 352), (3, 602), (2, 183), (2, 2604), (2, 241), (2, 242), (3, 1757), (4, 665), (2, 532), (4, 1946), (2, 2854), (3, 1157), (0, 5000), (1, 311), (4, 832), (2, 622), (2, 37), (3, 3167), (4, 4572), (0, 5000), (3, 223), (3, 1146), (3, 3047), (3, 220), (1, 90), (1, 517), (2, 499), (1, 464), (0, 5000), (3, 4214), (2, 498), (0, 5000), (3, 1004), (3, 1704), (4, 1263), (3, 3113), (1, 500), (3, 3153), (2, 2623), (2, 453), (2, 330), (1, 507), (0, 5000), (0, 5000), (3, 1160), (4, 2906), (1, 6), (3, 11), (1, 585), (3, 3502), (1, 544), (2, 401), (4, 3203), (1, 580), (3, 304), (4, 347), (1, 402), (2, 248), (2, 45), (3, 3065), (2, 114), (1, 32), (3, 49), (0, 5000), (1, 599), (3, 2305), (3, 1116), (2, 601), (2, 192), (3, 118), (2, 301), (2, 153), (2, 216), (4, 1246), (1, 536), (4, 569), (3, 1751), (1, 4529), (2, 615), (2, 11), (3, 331), (2, 264), (1, 596), (2, 185), (4, 977), (1, 4496), (3, 1130), (3, 1090), (1, 330), (4, 3017), (0, 5000), (1, 494), (3, 116), (0, 5000), (1, 229), (1, 4732), (2, 4686), (1, 9), (3, 2485)]

# Test2
# [(2, 4269), (3, 811), (3, 750), (1, 119), (3, 1218), (0, 5000), (3, 1002), (3, 816), (4, 2864), (2, 613), (3, 464), (2, 179), (4, 4929), (2, 218), (2, 166), (4, 2204), (2, 297), (3, 298), (3, 872), (2, 235), (2, 260), (2, 255), (4, 1710), (3, 327), (4, 2086), (4, 1761), (2, 267), (3, 3202), (2, 146), (3, 393), (2, 269), (4, 3070), (3, 2734), (1, 108), (4, 2469), (2, 162), (2, 129), (2, 142), (3, 782), (4, 1280), (2, 311), (3, 324), (3, 340), (2, 231), (2, 612), (1, 73), (2, 180), (3, 491), (1, 120), (3, 3860), (1, 20), (4, 2815), (3, 489), (3, 995), (1, 49), (3, 353), (2, 247), (1, 103), (1, 12), (1, 94), (2, 156), (0, 5000), (3, 4411), (2, 2283), (0, 5000), (3, 959), (1, 1413), (4, 1590), (4, 3223), (1, 69), (2, 194), (1, 6), (4, 3398), (1, 34), (1, 6), (1, 92), (0, 5000), (3, 480), (1, 45), (4, 1744), (1, 1425), (3, 3483), (2, 316), (2, 590), (4, 3178), (3, 720), (4, 2360), (4, 1268), (3, 978), (3, 340), (3, 1263), (2, 163), (4, 3431), (2, 280), (2, 558), (3, 1222), (2, 163), (1, 128), (3, 304), (4, 1556)]

#Basic agent 1
#[(3, 8857), (3, 17471), (2, 10776), (0, 0), (3, 2679), (1, 5943), (1, 10936), (4, 84013), (3, 17602), (3, 17), (4, 33047), (2, 1388), (4, 23279), (3, 39898), (4, 79802), (3, 28252), (2, 88250), (2, 9512), (4, 38089), (1, 5492), (3, 43234), (4, 56279), (2, 1532), (3, 19713), (1, 10842), (1, 86125), (2, 1172), (3, 1699), (2, 48312), (3, 6903), (3, 6569), (0, 0), (3, 43044), (2, 8655), (3, 30332), (1, 5881), (1, 959), (2, 2046), (1, 5534), (2, 1188), (1, 2889), (4, 34185), (1, 2936), (4, 64399), (3, 42165), (1, 83194), (1, 1278), (4, 40621), (3, 8882), (2, 36), (2, 3994), (2, 1908), (2, 6070), (3, 6417), (4, 35212), (3, 6806), (4, 10068), (4, 13406), (2, 84781), (2, 962), (3, 6729), (3, 41007), (3, 19119), (2, 44447), (1, 8184), (2, 44926), (3, 77350), (2, 11167), (1, 9697), (4, 74062), (2, 87586), (1, 2117), (1, 9605), (4, 16411), (2, 7436), (2, 1413), (3, 82358), (1, 2183), (1, 77722), (1, 1231), (4, 34049), (4, 69979), (3, 20058), (2, 7192), (0, 0), (3, 18541), (3, 840), (1, 327), (2, 6285), (3, 44046), (3, 72792), (2, 8933), (3, 50492), (2, 10926), (4, 15489), (3, 67309), (2, 2301), (4, 16748), (4, 22303), (3, 19284)]
# Basic agent 2
#[(2, 5298), (3, 12528), (3, 14393), (0, 0), (2, 9921), (3, 48703), (1, 2261), (2, 5429), (2, 9769), (4, 37048), (3, 17675), (1, 1075), (3, 12976), (1, 642), (2, 10948), (2, 2673), (2, 9759), (1, 2011), (1, 469), (2, 3084), (1, 26303), (0, 0), (1, 1260), (2, 5359), (1, 2123), (1, 1314), (2, 4321), (3, 8641), (0, 0), (2, 2770), (1, 25925), (4, 27558), (2, 4036), (3, 21163), (0, 0), (1, 1923), (3, 17080), (2, 2887), (4, 30474), (3, 15228), (1, 25232), (2, 2239), (0, 0), (2, 5205), (4, 27753), (4, 27762), (0, 0), (2, 10470), (4, 44529), (1, 1602), (3, 18491), (1, 1932), (1, 1716), (1, 2060), (1, 1301), (3, 6420), (4, 33446), (4, 55448), (3, 15431), (4, 22435), (3, 59585), (4, 63214), (0, 0), (3, 13215), (1, 24551), (3, 60053), (2, 10830), (2, 40764), (1, 25898), (1, 1407), (3, 20766), (2, 2297), (3, 6856), (1, 795), (3, 58016), (4, 58834), (3, 19024), (3, 72921), (2, 3931), (1, 23943), (2, 3758), (4, 63061), (3, 15018), (1, 1489), (1, 1122), (3, 45115), (4, 51652), (2, 2385), (4, 41933), (3, 5361), (2, 11325), (1, 801), (4, 30922), (1, 343), (4, 54662), (1, 1797), (3, 14484), (2, 4268), (3, 21520), (2, 4497)]


