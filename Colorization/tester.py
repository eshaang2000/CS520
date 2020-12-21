import tensorflow as tf
from keras.preprocessing.image import img_to_array, load_img
from skimage.transform import resize
from skimage.io import imsave, imshow
import numpy as np
from skimage.color import rgb2lab, lab2rgb
from PIL import Image



def saveImageFromArray(arr, mode, name):
    if mode == 1:
        img = Image.fromarray(arr.astype('uint8'), 'RGB')
        img.save(name)
    else:
        img = Image.fromarray(arr.astype('uint8'), 'LA')
        img.save(name)

def getArray(image):
    return np.asarray(image)


model = tf.keras.models.load_model('auto.model/',
                                   custom_objects=None,
                                   compile=True)

ima = []

i = getArray(load_img('please.png')) #test data grayscale image
# i = resize(i, (256, 256)) # we
ima.append(i)
print(ima)
ima = np.array(ima)
ima = rgb2lab(1.0 / 255 * ima)[:, :, :, 0]
ima = ima.reshape(ima.shape + (1,))
#we then try to predict the AB values as we already have the L values
output = model.predict(ima)
output = output * 128
result = np.zeros((256, 256, 3)) #rgb values dimension
#we then fill in the LAB values using the data we already habe
result[:, :, 0] = ima[0][:, :, 0]
result[:, :, 1:] = output[0]
# result = lab2rgb(result)*255
# # print(type(result))
# # print(np.shape(result))
# # print(lab2rgb(result)*255)
# # saveImageFromArray(result, 1, "result.png")
imsave("result.png", lab2rgb(result))
