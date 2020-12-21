# import warnings filter
from warnings import simplefilter
import math
from collections import Counter
from PIL import Image
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

path = "data.png"
image = Image.open(path)


def convertImage(image):
    return image.convert('LA')


def getArray(image):
    return np.asarray(image)


# returns array of partitioned data
def partitionImage(image):
    d = getArray(image)
    p = image.width / 2
    p = int(p)
    train = np.zeros((image.height, p, len(d[0][0])))
    test = np.zeros((image.height, p, len(d[0][0])))
    for i in range(len(train)):
        for j in range(p):
            train[i][j] = d[i][j]
    for i in range(len(train)):
        for j in range(p):
            test[i][j] = d[i][j + p]
    return train, test


# t = partitionImage(image)
# img = Image.fromarray(t.astype('uint8'), 'RGB')
# img.save('my.jpg')


def getInitialCentroids():  # returns one random centroid
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def getInitialCentroidsBlack():
    return (random.randint(0, 255), 255)


def getKCentroids(k):
    ans = []
    i = 0
    while i != k:
        c1 = getInitialCentroids()
        if c1 in ans:
            continue
        ans.append(c1)
        i += 1
    return ans


def getKCentroidsBlack(k):
    ans = []
    i = 0
    while i != k:
        c1 = getInitialCentroids()
        if c1 in ans:
            continue
        ans.append(c1)
        i += 1
    return ans


def getDistance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]
    z1 = p1[2]
    z2 = p2[2]

    dist = math.sqrt(math.pow(x2 - x1, 2) +
                     math.pow(y2 - y1, 2) +
                     math.pow(z2 - z1, 2) * 1.0)
    return dist


def getDistanceBlack(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]

    dist = math.sqrt(math.pow(x2 - x1, 2) +
                     math.pow(y2 - y1, 2) * 1.0)
    return dist


def average(d1, data):
    n = len(d1)
    a1 = 0
    a2 = 0
    a3 = 0
    for i in d1:
        a1 += data[i[0]][i[1]][0]
        a2 += data[i[0]][i[1]][1]
        a3 += data[i[0]][i[1]][2]
    a1 = a1 / n
    a2 = a2 / n
    a3 = a3 / n
    a1 = round(a1)
    a2 = round(a2)
    a3 = round(a3)
    t = [a1, a2, a3]
    return t


def averageBlack(d1, data):
    n = len(d1)
    a1 = 0
    a2 = 0
    for i in d1:
        a1 += data[i[0]][i[1]][0]
        a2 += data[i[0]][i[1]][1]
    a1 = a1 / n
    a2 = a2 / n
    a1 = round(a1)
    a2 = round(a2)
    t = [a1, a2]
    return t


def classify(C, dataPoint):
    # find the centroid that is of minimum distance for that data point. C is a list of centroids that have to be
    # gone through
    minim = 100000000
    minDist = 10000000
    for j in range(len(C)):
        dist = getDistance(dataPoint, C[j])
        if minDist > dist:
            minim = j
            minDist = dist

    return minim


def classifyBlack(C, dataPoint):
    # find the centroid that is of minimum distance for that data point. C is a list of centroids that have to be
    # gone through
    minim = 100000000
    minDist = 10000000
    for j in range(len(C)):
        dist = getDistanceBlack(dataPoint, C[j])
        if minDist > dist:
            minim = j
            minDist = dist

    return minim


def saveImageFromArray(arr, mode, name):
    if mode == 1:
        img = Image.fromarray(arr.astype('uint8'), 'RGB')
        img.save(name)
    else:
        img = Image.fromarray(arr.astype('uint8'), 'LA')
        img.save(name)


#
# data = getArray(image)
#


# find the loss when converted to gray scale
def loss(ans, test):
    d = 0
    for i in range(len(ans)):
        for j in range((len(ans[0]))):
            d += (ans[i][j][0] - test[i][j][0]) ** 2 + (ans[i][j][1] - test[i][j][1]) ** 2 + (
                    ans[i][j][2] - test[i][j][2]) ** 2
    d = math.sqrt(d)
    return d / i / j


# k = 20
# We now write the code for k means clustering
# returns image array, Centroids, things that correcpond to the centroid though finding that is pretty easy
def kMeansClustering(k, data):
    C = getKCentroids(k)
    iter = 0
    while iter != 10:
        flag = True
        print("starting iter no " + str(iter))
        C1 = []
        for i in range(k):
            C1.append(set())
        for j in range(len(data)):
            for i in range(len(data[0])):
                index = classify(C, data[j][i])
                # print(index)
                C1[index].add((j, i))
        cOld = C.copy()
        # print(cOld)
        for i in range(len(C1)):
            if len(C1[i]) == 0:
                continue
            ctemp = average(C1[i], data)
            C[i] = ctemp
        # print(C)
        for i in range(len(C)):
            # print(C[i])
            # print(cOld[i])
            # if not np.array_equal(C[i], cOld[i]):
            #     flag = False
            #     break
            for j in range(len(C[i])):
                if abs(C[i][j] - cOld[i][j]) > 3:
                    flag = False
                    break

        # for i in range(len(cOld)):
        #     print(C[i])
        #     print(cOld[i])
        #     if C[i] != cOld[i]:
        #         flag = False
        #         break
        if flag:  # we have reached convergence
            break
        iter += 1
    # print(C)
    image1 = np.zeros((len(data), len(data[0]), 3))
    l = 0
    for i in C1:
        for j in i:
            image1[j[0]][j[1]] = C[l]
        l += 1
    return image1, C, C1


def kMeansClusteringBlack(k, data):
    C = getKCentroidsBlack(k)
    iter = 0
    while iter != 20:
        print("starting iter no " + str(iter))
        C1 = []
        for i in range(k):
            C1.append(set())
        for j in range(len(data)):
            for i in range(len(data[0])):
                index = classifyBlack(C, data[j][i])
                # print(index)
                C1[index].add((j, i))
        for i in range(len(C1)):
            if len(C1[i]) == 0:
                continue
            ctemp = averageBlack(C1[i], data)
            C[i] = ctemp
        # print(C)
        iter += 1
    # print(C)
    image1 = np.zeros((len(data), len(data[0]), 2))
    l = 0
    for i in C1:
        for j in i:
            image1[j[0]][j[1]] = C[l]
        l += 1
    return image1, C, C1


# make a matrix of averages of the gray scale array
def grayAverage(grayMatrix):
    avg = np.zeros((len(grayMatrix), len(grayMatrix[0]), 2))
    for i in range(1, len(grayMatrix) - 1):
        for j in range(1, len(grayMatrix[0]) - 1):
            a = grayMatrix[i][j][0]
            a += grayMatrix[i + 1][j][0]
            a += grayMatrix[i - 1][j][0]
            a += grayMatrix[i + 1][j + 1][0]
            a += grayMatrix[i - 1][j + 1][0]
            a += grayMatrix[i + 1][j - 1][0]
            a += grayMatrix[i - 1][j - 1][0]
            a += grayMatrix[i][j - 1][0]
            a += grayMatrix[i][j + 1][0]
            a /= 9
            avg[i][j] = a
            avg[i][j][1] = grayMatrix[i][j][1]
    return avg


def stripGray(grayData):
    dope = np.zeros((len(grayData), len(grayData[0])))
    dope.astype(np.uint8)
    for i in range(len(grayData)):
        for j in range(len(grayData[0])):
            dope[i][j] = grayData[i][j][0]
    return dope


def getColors(indexes, coloredImage):
    colors = []
    for i in range(len(indexes)):
        x = indexes[i][0]
        y = indexes[i][1]
        colors.append(coloredImage[x][y])
    return colors


def convertRGB(r, g, b):
    return 65536 * r + 256 * g + b


def convertToRGB(rgb):
    r = [rgb >> 16 & 255, rgb >> 8 & 255, rgb & 255]
    return r


def getProbabilities(colors, C):
    co = [tuple(i) for i in colors]
    # freqDict = Counter(co)
    probs = dict()
    dist = []
    # for i in co:
    #     temp = 0
    #     mini = getDistance(i, C[0])
    #     for j in range(len(C)):
    #         if getDistance(i, C[j]) < mini:
    #             temp = j
    #     dist.append(temp)
    for i in C:
        dist.append(1/getDistance(i, co[0]))
        # print(dist)
    # print(dist)
    tot = 0
    for i in dist:
        tot+=i
    print(tot)
    j = 0
    for i in C:
        probs[tuple(i)] = (dist[j])/tot
        j+=1

    # mkey = None
    # tot = 0
    p = []
    i = []
    # for (key, val) in freqDict.items():
    #     tot += val
    # for (key, val) in freqDict.items():
    #     probs[key] = val / tot

    for (key, val) in probs.items():
        p.append(val)
        i.append(int(convertRGB(key[0], key[1], key[2])))
    print(p)
    print(i)
    [i1, i2]= sorted(range(len(p)), key=lambda i: p[i], reverse=True)[:2]
    p2 = [p[i1], p[i2]]
    i3 = [i[i1], i[i2]]

    ans = random.choices(i3, p2)
    print(ans)
    print(ans[0])
    ans1 = convertToRGB(ans[0])
    return ans1


# outputs the majority color
def majority(colors):
    co = [tuple(i) for i in colors]
    freqDict = Counter(co)
    maxim = 0
    mkey = None
    for (key, val) in freqDict.items():
        if val > maxim:
            mkey = key
            maxim = val
    return mkey


i = convertImage(image)  # this is an image that is returned in gray scale
trainGray, testGray = partitionImage(i)  # we split his image in half - this is the gray scale array
trainRGB, testRGB = partitionImage(image)  # this is the rgb split - this is the gray scale array
trainAvgGray = grayAverage(trainGray)

imageArray = getArray(image)
ima, C, C1 = kMeansClustering(20, trainRGB)
# # saveImageFromArray(ima, 1)
# saveImageFromArray(trainRGB, 1, "rbgtrain.png")
# saveImageFromArray(ima, 1, "rgbklustered.png")

# make a huge list that can be trained and the results are then got
temp = []
tempIndex = dict()
for i in range(len(trainAvgGray)):
    for j in range(len(trainAvgGray[0])):
        temp.append(trainAvgGray[i][j])
        tempIndex[len(temp) - 1] = (i, j)
#
# indexes = [(0, 0), (1, 0), (1, 1)]
# print(getColors(indexes, trainRGB))
# print(majority(getColors(indexes, trainRGB)))


# the machine learning model is ready
print("Start kd tree training")
temp1 = np.asarray(temp)
nn = NearestNeighbors(1, algorithm='kd_tree')
k = nn.fit(temp1)

ans = np.zeros((len(testGray), len(testGray[0]), 3))
# test = np.asarray(testGray[300][300])
# print(test)
# values, indexs = nn.kneighbors(test.reshape(1, -1), 6)
# indexes = []
# for k in indexs[0]:
#     indexes.append(tempIndex[k])
    # print(indexes)
# ans[300][300] = majority(getColors(indexes, ima))
# print(getProbabilities(getColors(indexes, ima)))
# ans[300][300] = getProbabilities(getColors(indexes, ima))
# print(300, 300)
# print(ans[300][300])


for i in range(len(testGray)):
    for j in range(len(testGray[0])):
        test = np.asarray(testGray[i][j])
        print("This is the test")
        print(test)
        values, indexs = nn.kneighbors(test.reshape(1, -1), 1)
        indexes = []
        # print(indexes)
        for k in indexs[0]:
            indexes.append(tempIndex[k])
        # print(indexes)
        b = getProbabilities(getColors(indexes, trainRGB), C)
        print(b)
        ans[i][j] = b
        print(i, j)

print(ans)
print(loss(ans, testRGB))
ans2 = np.concatenate((trainRGB, ans), axis=1)
saveImageFromArray(ans, 1, "ans.png")
saveImageFromArray(ans2, 1, "ans9.png")

