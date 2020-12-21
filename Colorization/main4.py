import numpy as np
from keras.preprocessing.image import ImageDataGenerator
from skimage.color import rgb2lab
from keras.layers import Conv2D, UpSampling2D
from keras.models import Sequential
import tensorflow as tf
import matplotlib as plt

path = 'germans/'

# I first normalize the images
train_gen = ImageDataGenerator(
    rescale=1. / 255)  # the relu activation function goes from 0 to 1. Hence have to normalize it

# Resize images, if needed
train = train_gen.flow_from_directory(path, target_size=(256, 256), batch_size=151, class_mode=None)

# Convert from RGB to Lab

L = []
AB = []
print(len(train))
for img in train[0]:
    try:
        lab = rgb2lab(img)
        L.append(lab[:, :, 0])  # this is the gray scale
        AB.append(lab[:, :, 1:] / 128)  # A and B values range from -127 to 128,
        # so we divide the values by 128 to restrict values to between -1 and 1.
    except:
        print('error')
L = np.array(L)
AB = np.array(AB)
L = L.reshape(L.shape + (1,))  # dimensions to be the same for X and Y
print(L.shape)
print(AB.shape)
print(L)
print(AB)

# Encoder
# this encoding the imade to the basic level and hence removing "noise"
m = Sequential()
m.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2, input_shape=(256, 256, 1)))
m.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
m.add(Conv2D(128, (3, 3), activation='relu', padding='same', strides=2))
m.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
print("Decoding")
# Decoder
m.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
m.add(UpSampling2D((2, 2)))
m.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
m.add(Conv2D(16, (3, 3), activation='relu', padding='same'))
m.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
m.add(UpSampling2D((2, 2)))
m.compile(optimizer='SGD', loss='mse', metrics=['accuracy'])
m.summary()

m.fit(L, AB, validation_split=0.1, epochs=8, batch_size=36)
m.save('auto.model')
