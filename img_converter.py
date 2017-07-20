import cv2
import numpy as np
import argparse
import os

#https://habrahabr.ru/post/144416/
parser = argparse.ArgumentParser(description='Positive/negative images preparation for HAAR cascade')
subpasers = parser.add_subparsers(help='List of commands')

parser.add_argument('-p', '--path', required=True, help='Path to your images')
parser.add_argument('-t', '--type', required=True, help='Specify whether positive or negative images are processed (type "pos" or "neg")')
parser.add_argument('-wd', '--width', required=False, type = int, help='Image width (default: positive - 60 | negative - 500)')
parser.add_argument('-hg', '--height', required=False, type = int, help='Image height (default: positive - 90 | negative - 600)')

args = parser.parse_args()


def store_raw_images(imgs_path, imgs_type):

    imgs_format = '.jpg'

    if imgs_type == 'pos':
        width = args.width if args.width else 60
        height = args.height if args.height else 90
    elif imgs_type == 'neg':
        width = int(args.width) if args.width else 500
        height = int(args.height) if args.height else 600

    # print(width, height)

    if any([img[0:3] == imgs_type for img in os.listdir(imgs_path)]):
        current_imgs = list(filter(lambda x: x[0:3] == imgs_type, os.listdir(imgs_path)))
        name_index = max(list(map(lambda x: int(x[4:-4]), current_imgs))) + 1
        imgs = list(filter(lambda x: x[0:3] != imgs_type, os.listdir(imgs_path)))
    else:
        name_index = 1
        imgs = os.listdir(imgs_path)

    for img in imgs:
        try:
            # Grayscaling and resizing
            grayscaled = cv2.imread(imgs_path + img, cv2.IMREAD_GRAYSCALE)
            resized = cv2.resize(grayscaled, (width, height))
            cv2.imwrite(imgs_path + imgs_type + '-' + str(name_index) + imgs_format, resized)
            name_index += 1

            # Deleting origin image
            os.remove(imgs_path + img)

        except Exception as e:
            os.remove(imgs_path + img)


store_raw_images(args.path, args.type)



def create_descriptions(path):
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
