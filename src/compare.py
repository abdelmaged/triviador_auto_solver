#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
import shutil
import cv2
import ImageChops
from subprocess import call
import math, operator

path = "/home/abdelmaged/saif/search/"
path_found = "/home/abdelmaged/saif/found/"
path_cropped = "/home/abdelmaged/saif/cropped/"
path_ans = "/home/abdelmaged/saif/ans/"
tmp = "/home/abdelmaged/saif/tmp/"
val = "1972"


def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"

    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))


def equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None


if __name__ == '__main__':
    im = Image.open(path_found + "1.png")
    for fname in sorted(os.listdir(path_found)):
        mi = Image.open(path_found + fname)
        # ImageChops.difference(im, mi).getbbox()
        print fname, rmsdiff(im, mi), equal(im, mi)
