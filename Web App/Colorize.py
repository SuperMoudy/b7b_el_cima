#!/usr/bin/env python

import cv2
import numpy as np
import keras
from skimage import color
from scipy.misc import imresize
from keras.models import load_model


def lab_to_rgb(l_layer, ab_layers, img_size):
    new_img = np.zeros((img_size,img_size,2))
    rescaled_l = np.zeros((img_size,img_size,1))
    for i in range(len(ab_layers)):
        for j in range(len(ab_layers[i])):
            p = ab_layers[i,j]
            new_img[i,j] = [(p[0] +1) / 2 * 255 - 128, (p[1] +1) / 2 * 255 - 128]
            rescaled_l[i,j] = [(l_layer[i,j] + 1) * 50]

    new_img = np.concatenate((rescaled_l,new_img),axis=-1)
    new_img = color.lab2rgb(new_img) * 255
    new_img = new_img.astype('uint8')
    return new_img


def colorize(input_path, output_path):
    model = load_model('./models/movieColor_03-0.78.hdf5')
    img_rgb = np.array(cv2.imread(input_path)[:,:,::-1], dtype=np.float32)/255
    size = img_rgb.shape[:2]
    img_rgb = cv2.resize(img_rgb, (256, 256))
    img_gray = color.rgb2gray(img_rgb)[..., np.newaxis] * 2 - 1
    output = model.predict(np.array([img_gray]))
    new_img = lab_to_rgb(output[0][:, :, 0], output[0][:, :, 1:], 256)

    cv2.imwrite(output_path, cv2.resize(new_img, (size[1], size[0]))[:,:,::-1])
