### https://www.youtube.com/watch?v=t0HOVLK30xQ

from cv2.cv2 import *
import numpy as np
import os


def store_raw_images(path):

    new_name = 16
    for img in os.listdir(path):
        try:
            # Grayscaling and resizin
            grayscaled = imread(path + img, IMREAD_GRAYSCALE)
            resized = resize(grayscaled, (60,90)) if path[0:-1] == 'pos' else resize(grayscaled, (500,600))
            imwrite(path + path[0:-1] + '-' + str(new_name) + '.jpg', resized)
            new_name += 1

            # Deleting origin image
            os.remove(path + img)

        except Exception as e:
            print(str(e))
            os.remove(path + img)

# store_raw_images('neg/')
store_raw_images('pos/')

def create_pos_n_neg(path):
    for img in os.listdir(path):
        if path[0:-1] == 'neg':
            line = path + img + '\n'
            with open('bg.txt', 'a') as f:
                f.write(line)

        elif path[0:-1] == 'pos':
            line = path + img + ' 1 0 0 80 120\n'
            with open('info.dat', 'a') as f:
                f.write(line)

# create_pos_n_neg('neg/')
# create_pos_n_neg('pos/')
