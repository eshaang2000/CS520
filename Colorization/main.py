import math
from PIL import Image
import numpy as np
import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors


path = "data.jpg"
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


def saveImageFromArray(arr, mode):
    if mode == 1:
        img = Image.fromarray(arr.astype('uint8'), 'RGB')
        img.save('my.jpg')
    else:
        print(len(arr[0][0]))
        img = Image.fromarray(arr.astype('uint8'), 'L')
        img.save('my.jpg')


#
# data = getArray(image)
#

# k = 20
# We now write the code for k means clustering
# returns image array, Centroids, things that correcpond to the centroid though finding that is pretty easy
def kMeansClustering(k, data):
    C = getKCentroids(k)
    iter = 0
    while iter != 3:
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


# make a matrix of averages of the gray scale array
def grayAverage(grayMatrix):
    avg = np.zeros((len(grayMatrix), len(grayMatrix[0]), 2))
    for i in range(1, len(grayMatrix)-1):
        for j in range(1, len(grayMatrix[0])-1):
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



"""
1. Write code to get a single number that would get the rep of the 3x3 data
"""

i = convertImage(image)  # this is an image that is returned in gray scale
trainGray, testGray = partitionImage(i)  # we split his image in half - this is the gray scale array
trainRGB, testRGB = partitionImage(image)  # this is the rgb split - this is the gray scale array
trainAvgGray = grayAverage(trainGray)

# print(trainAvgGray)
# df = pd.DataFrame(trainAvgGray)
# print(df)
print(trainAvgGray)

temp = []
for i in trainAvgGray:
    for j in i:
        temp.append(j)
temp1 = np.asarray(temp)
for i in [291183, 185444, 261385, 313990, 204820]:
    print(temp1[i])
# nn = NearestNeighbors(5, algorithm='kd_tree')
# k = nn.fit(temp1)
# test = np.array([234, 255])
# print("here")
# print(nn.kneighbors(test.reshape(1, -1), 5))
# print("now here")
# imag, C, C1 = kMeansClustering(10, trainRGB)
# trainG = np.zeros((len(trainGray), len(trainGray[0]), 1))
# for i in range(len(trainGray)):
#     for j in range(len(trainGray[0])):
#         trainG[i][j] = g[i][j][0]


# df = pd.DataFrame(g.reshape(len(g), len(g[0])))
# df = pd.DataFrame(g.reshape(2, 2))
## save to xlsx file
#[[291183, 185444, 261385, 313990, 204820]]