
import cv2
import progressbar
import subprocess as sp
import argparse
import os


parser = argparse.ArgumentParser(description='Easy dataset creation for HAAR cascades v0.1')
subpasers = parser.add_subparsers(dest='command', help='List of commands')

image_parser = subpasers.add_parser('prepareimages', help='Crop and rescale positive/negative images')
image_parser.add_argument('-p', '--path', required=True, help='Path to your images')
image_parser.add_argument('-t', '--type', required=True, help='Specify whether positive or negative images are '
                                                               'processed (type "pos" or "neg")')
image_parser.add_argument('-wd', '--width', required=False, type=int, help='Image width (default: positive - 60 | '
                                                                            'negative - 500)')
image_parser.add_argument('-hg', '--height', required=False, type=int, help='Image height (default: positive - 90 | '
                                                                             'negative - 600)')

description_parser = subpasers.add_parser('createdescriptions', help='Create description files for positive/negative images')
description_parser.add_argument('-p', '--path', required=True, help='Path to folder with negative images')
description_parser.add_argument('-t', '--type', required=True, help='Specify whether positive or negative images are '
                                                             'processed (type "pos" or "neg")')
description_parser.add_argument('-wd', '--width', required=False, type=int, help='Positive image width ('
                                                                                             'default: 60)')
description_parser.add_argument('-hg', '--height', required=False, type=int, help='>Positive image height '
                                                                                              '(default: 90)')
description_parser.add_argument('-f', '--format', required=False, default='txt', help='Specify format of file')

info_parser = subpasers.add_parser('createinfo', help='Create info images and info text file')
info_parser.add_argument('-p', '--path', required = True, help='Path to positive images folder')
info_parser.add_argument('-bg', '--background', required=True, help='Description file for negative images')
info_parser.add_argument('-o', '--output', required=True, help='Output folder for info files')
info_parser.add_argument('-mx', '--maxX', required=False, default=0, type=float, help='Max X angle (default: 0)')
info_parser.add_argument('-my', '--maxY', required=False, default=0, type=float, help='Max Y angle (default: 0)')
info_parser.add_argument('-mz', '--maxZ', required=False, default=0, type=float, help='Max Z angle (default: 0)')
info_parser.add_argument('-n', '--num', required=False, default=200, type=int, help='Number of objects fot each positive image (default: 200)')
info_parser.add_argument('-wd', '--width', required=False, default=20, type=int, help='Ratio width (default: 20))')
info_parser.add_argument('-hg', '--height', required=False, default=20, type=int, help='Ratio height (default: 20)')
info_parser.add_argument('-tr', '--threshold', required=False, default=0, type=int, help='Background threshold (default: 0)')

args = parser.parse_args()

if args.command in ('prepareimages', 'createdescriptions'):
    if args.type == 'pos':
        width = args.width if args.width else 60
        height = args.height if args.height else 90
    elif args.type == 'neg':
        width = args.width if args.width else 500
        height = args.height if args.height else 600
    else:
        raise(TypeError("Type should be 'pos' or 'neg'. Usage example:\n"
                        "user: python3 img_converter.py list -p positives/ -t pos"))

# Progress bar
bar = progressbar.ProgressBar()

def store_raw_images(path, type):
    imgs_format = '.jpg'

    if any([img[0:3] == type for img in os.listdir(path)]):
        current_imgs = list(filter(lambda x: x[0:3] == type, os.listdir(path)))
        name_index = max(list(map(lambda x: int(x[4:-4]), current_imgs))) + 1
        imgs = list(filter(lambda x: x[0:3] != type, os.listdir(path)))
    else:
        name_index = 1
        imgs = os.listdir(path)

    for img in bar(imgs):
        try:
            # Grayscaling and resizing
            grayscaled = cv2.imread(path + img, cv2.IMREAD_GRAYSCALE)
            resized = cv2.resize(grayscaled, (width, height))
            cv2.imwrite(path + type + '-' + str(name_index) + imgs_format, resized)
            name_index += 1

            # Deleting origin image
            os.remove(path + img)

        except Exception as e:
            os.remove(path + img)


def create_descriptions(path, type):
    if type == 'neg':
        if 'bg.' + args.format in os.listdir('.'):
            os.remove('bg.' + args.format)
        for img in bar(os.listdir(path)):
            line = path + img + '\n'
            with open('bg.' + args.format, 'a') as f:
                f.write(line)

    elif type == 'pos':
        if 'info.' + args.format in os.listdir('.'):
            os.remove('info.' + args.format)
        for img in bar(os.listdir(path)):
            line = path + img + ' 1 0 0 ' + str(width) + ' ' + str(height) + '\n'
            with open('info.' + args.format, 'a') as f:
                f.write(line)

def create_info(path, background, output, maxX, maxY, maxZ, number, width, height, threshold):
    info_index = 1

    for img in bar(os.listdir(path)):
        path_to_image = path + img
        info_name = 'info'+str(info_index)
        info_output = output + info_name

        sp.run(
            ['opencv_createsamples', '-img', path_to_image, '-bg', background, '-info', info_output, '-pngoutput',
             'info', '-maxxangle', maxX, '-maxyangle', maxY, '-maxzangle', maxZ, '-num', number, '-w', width,
             '-h', height, '-bgthresh', threshold])


if args.command == 'prepareimages':
    store_raw_images(args.path, args.type)
elif args.command == 'createdescriptions':
    create_descriptions(args.path, args.type)
elif args.command == 'createinfo':
    create_info(args.path, args.background, args.output, args.maxX, args.maxY, args.maxZ, args.num, args.width, args.height, args.threshold)
