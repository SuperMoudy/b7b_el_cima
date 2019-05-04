import cv2
import numpy as np
from keras.models import load_model
from skimage import color



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


def colorize_video(file_name, out_name):
    model = load_model('./models/movieColor.h5')
    vidcap = cv2.VideoCapture(file_name)
    frame_width = int(vidcap.get(3))
    frame_height = int(vidcap.get(4))
    out = cv2.VideoWriter(out_name,cv2.VideoWriter_fourcc('H','2','6','4'), 30, (frame_width,frame_height))
    success, image = vidcap.read()
    no_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('number of frames', no_of_frames)
    n = 30*2
    while success and n>0:
        img_rgb = np.array(image[:,:,::-1], dtype=np.float32)/255
        img_rgb = cv2.resize(img_rgb, (256, 256))
        img_gray = color.rgb2gray(img_rgb)[..., np.newaxis] * 2 - 1
        output = model.predict(np.array([img_gray]))
        new_img = lab_to_rgb(output[0][:, :, 0], output[0][:, :, 1:], 256)
        new_img = cv2.resize(new_img, (frame_width, frame_height))[:,:,::-1]
        out.write(new_img)
        success, image = vidcap.read()
        print(n)
        n-=1
    vidcap.release()
    out.release()
