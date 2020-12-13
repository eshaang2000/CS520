import math

from PIL import Image
import numpy as np
import random
import pandas as pd

path = "data.jpg"
image = Image.open(path)


def convertImage(image):
    return image.convert('LA')


def getArray(image):
    return np.asarray(image)


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


data = getArray(image)
k = 20
# We now write the code for k means clustering
C = getKCentroids(k)
iter = 0
while iter != 1:
    # # r = input()
    # if r == "done":
    #     break
    print(C)
    C1 = []
    for i in range(k):
        C1.append(set())
    for j in range(len(data)):
        for i in range(len(data[0])):
            index = classify(C, data[j][i])
            # print(index)
            C1[index].add((j, i))
        print(j)
    # print(C1)
    for i in range(len(C1)):
        if len(C1[i]) == 0:
            continue
        ctemp = average(C1[i], data)
        C[i] = ctemp
    print(C)
    iter += 1
print(C)
# print(C1)
image1 = np.zeros((image.height, image.width, 3))
l = 0
for i in C1:
    for j in i:
        image1[j[0]][j[1]] = C[l] #data[j[0]][j[1]]
    l += 1
if np.array_equal(image1, data):
    print("hahaah")

# for i in range(len(image1)):
#     for j in range(len(data)):
#         if data[i][j][0] == image1[i][j][0] and data[i][j][1] == image1[i][j][1] and data[i][j][2] == image1[i][j][2]:
#             continue
#         else:
#             print("problen")
#             break
print(type(image1))
print(type(data))
img = Image.fromarray(image1.astype('uint8'), 'RGB')
img.save('my.jpg')
