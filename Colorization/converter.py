from PIL import Image
from skimage.io import imsave, imshow

path = "test.jpg"
image = Image.open(path)
from skimage.color import rgb2lab
import numpy as np


def convertImage(image):
    i = image.convert('LA')
    i.save("test.png")


def getArray(image):
    return np.asarray(image)


X = []
Y = []

lab = rgb2lab(image)
X.append(lab[:, :, 0])  # this is the gray scale
Y.append(lab[:, :, 1:] / 128)  # A and B values range from -127 to 128,
# so we divide the values by 128 to restrict values to between -1 and 1.

X = np.array(X)
print(X)
Y = np.array(Y)
X = X.reshape(X.shape + (1,))  # dimensions to be the same for X and Y
print(X)
X[0] = np.around(X[0])
# imshow(X[0], cmap = 'gray')
imsave("please.png", X[0])
convertImage(image)

