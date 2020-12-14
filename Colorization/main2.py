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


path = "data.png"
image = Image.open(path)
i = convertImage(image)  # this is an image that is returned in gray scale
trainGray, testGray = partitionImage(i)  # we split his image in half - this is the gray scale array
trainRGB, testRGB = partitionImage(image)  # this is the rgb split - this is the gray scale array
trainAvgGray = grayAverage(trainGray)
trainRGBsingle = np.zeros((len(trainRGB), len(trainRGB[0])))
testRGBsingle = np.zeros((len(trainRGB), len(trainRGB[0])))
for i in range(len(trainRGB)):
    for j in range(len(trainRGB[0])):
        trainRGBsingle[i][j] = convertRGB(trainRGB[i][j][0], trainRGB[i][j][1], trainRGB[i][j][2])

for i in range(len(testRGB)):
    for j in range(len(testRGB[0])):
        testRGBsingle[i][j] = convertRGB(testRGB[i][j][0], testRGB[i][j][1], testRGB[i][j][2])

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
t = np.asarray(temp)
t1 = np.asarray(temp1)
t1 = t1.reshape(-1, 1)
t = t.reshape(-1, 1)

t3 = np.asarray(temp3)
t4 = np.asarray(temp4)
t4 = t4.reshape(-1, 1)
t3 = t3.reshape(-1, 1)

regr.fit(temp, temp1)
print(regr.score(temp3, temp4))
