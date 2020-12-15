"""
1. I plan to use linear regression first to see if I can predict the color well
2. If not we can use some kind of neural network for this to work

1. Linear regression
"""

import math
from collections import Counter

from PIL import Image
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


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


def saveImageFromArray(arr, mode, name):
    if mode == 1:
        img = Image.fromarray(arr.astype('uint8'), 'RGB')
        img.save(name)
    else:
        img = Image.fromarray(arr.astype('uint8'), 'LA')
        img.save(name)


def convertRGB(r, g, b):
    return 65536 * r + 256 * g + b


def convertToRGB(rgb):
    r = [rgb >> 16 & 255, rgb >> 8 & 255, rgb & 255]
    return r


def grayAverage(grayMatrix):
    avg = np.zeros((len(grayMatrix), len(grayMatrix[0]), 2))
    for i in range(len(grayMatrix)):
        avg[i][0] = grayMatrix[i][0]
        avg[i][len(grayMatrix[0])-1] = grayMatrix[i][len(grayMatrix[0])-1]
    for i in range(len(grayMatrix[0])):
        avg[0][i] = grayMatrix[0][i]
        avg[len(grayMatrix)-1][i] = grayMatrix[len(grayMatrix)-1][i]
    # for i in range(len(grayMatrix)):
    #     avg[i][0] = grayMatrix[i][0]
    # for i in range(len(grayMatrix[0])):
    #     avg[0][i] = grayMatrix[0][i]

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
    print(avg)
    return avg


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
    minim = 100000000000
    minDist = 100000000000
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


def kMeansClustering(k, data):
    C = getKCentroids(k)
    iter = 0
    while iter != 10:
        print("starting iter no " + str(iter))
        C1 = []
        for i in range(k):
            C1.append(set())
        for j in range(len(data)):
            for i in range(len(data[0])):
                index = classify(C, data[j][i])
                # print(index)
                C1[index].add((j, i))
        for i in range(len(C1)):
            if len(C1[i]) == 0:
                continue
            ctemp = average(C1[i], data)
            C[i] = ctemp
        # print(C)
        iter += 1
    # print(C)
    image1 = np.zeros((len(data), len(data[0]), 3))
    l = 0
    for i in C1:
        for j in i:
            image1[j[0]][j[1]] = C[l]
        l += 1
    return image1, C, C1


path = "data.png"
image = Image.open(path)
i = convertImage(image)  # this is an image that is returned in gray scale
trainGray, testGray = partitionImage(i)  # we split his image in half - this is the gray scale array
trainRGB, testRGB = partitionImage(image)  # this is the rgb split - this is the gray scale array
trainAvgGray = grayAverage(trainGray)
trainRGBsingle = np.zeros((len(trainRGB), len(trainRGB[0])))
testRGBsingle = np.zeros((len(trainRGB), len(trainRGB[0])))
# trainRGB, C, C1 = kMeansClustering(30, trainRGB)
print(trainRGB)
for i in range(len(trainRGB)):
    for j in range(len(trainRGB[0])):
        trainRGBsingle[i][j] = convertRGB(trainRGB[i][j][0], trainRGB[i][j][1], trainRGB[i][j][2])

# for i in range(len(testRGB)):
#     for j in range(len(testRGB[0])):
#         testRGBsingle[i][j] = convertRGB(testRGB[i][j][0], testRGB[i][j][1], testRGB[i][j][2])

temp = []
tempIndex = dict()
temp1 = []
temp1Index = dict()
for i in range(len(trainAvgGray)):
    for j in range(len(trainAvgGray[0])):
        temp.append(trainAvgGray[i][j])
        tempIndex[len(temp) - 1] = (i, j)
for i in range(len(trainRGBsingle)):
    for j in range(len(trainRGBsingle[0])):
        temp1.append(trainRGBsingle[i][j])
        temp1Index[len(temp1) - 1] = (i, j)

temp3 = []
temp3Index = dict()
temp4 = []
temp4Index = dict()
for i in range(len(testGray)):
    for j in range(len(testGray[0])):
        temp3.append(testGray[i][j])
        temp3Index[len(temp3) - 1] = (i, j)

for i in range(len(testRGBsingle)):
    for j in range(len(testRGBsingle[0])):
        temp4.append(testRGBsingle[i][j])
        temp4Index[len(temp4) - 1] = (i, j)

regr = LinearRegression()
plt.scatter([i[0] for i in temp], temp1)
plt.show()
regr.fit(temp, temp1)
print(len(temp))
print(len(temp1))
# print(temp5)

temp5 = regr.predict(temp3)
ans = np.zeros((len(temp5)))
print(temp5)
for i in range(len(temp5)):
    temp5[i] = round(temp5[i])
ans = np.zeros((len(testRGB), len(testRGB[0]), 3))
print(temp5)
print(temp4[0])
print(convertToRGB(int(temp5[0])))
print(convertToRGB(int(temp4[0])))
for i in range(len(temp5)):
    z = temp4Index[i]
    x = z[0]
    y = z[1]
    ans[x][y] = convertToRGB(int(temp5[i]))
print(ans)
saveImageFromArray(ans, 1, "pls.png")
# for i in range(len(temp5)):
#     print(temp4[i])
# print(temp4Index[i])
# ans = regr.predict(temp5)
# print(ans)
print(regr.score(temp3, temp4))
