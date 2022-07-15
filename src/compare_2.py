#!/usr/bin/env python
"""Compare two aligned images of the same size.

Usage: python compare.py first-image second-image
"""

import sys
import os
from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average
import numpy as np
import cv2
import Image


path_found = "/home/abdelmaged/saif/found/"
path_cropped = "/home/abdelmaged/saif/cropped/"


def main():
    file1 = sys.argv[1]
    # file1 = "2.png"
    maged = 1000000000
    magedfile = ""
    for file2 in sorted(os.listdir(path_cropped)):
        im = cv2.imread(file1)
        k = cv2.imread(path_cropped + file2)
        h, w = k.shape[:2]

        mi = cv2.resize(im, (w, h))
        file3 = file1 + ".png"
        cv2.imwrite(file3, mi)
        # read images as 2D arrays (convert to grayscale for simplicity)
        img1 = to_grayscale(imread(file3).astype(float))
        img2 = to_grayscale(imread(path_cropped + file2).astype(float))
        # compare
        n_m, n_0 = compare_images(img1, img2)
        # print file2
        # print "Manhattan norm:", n_m, "/ per pixel:", n_m/img1.size
        # print "Zero norm:", n_0, "/ per pixel:", n_0*1.0/img1.size
        # print file2, n_m, n_m/img1.size, n_0, n_0*1.0/img1.size
        if(n_m/img1.size < maged):
            maged = n_m/img1.size
            magedfile = file2
            print file2, n_m, n_m/img1.size, n_0, n_0*1.0/img1.size

        os.remove(file3)
    im = Image.open(path_cropped + magedfile)
    im.show()


def compare_images(img1, img2):
    # normalize to compensate for exposure difference
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for scipy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)


def to_grayscale(arr):
    "If arr is a color image (3D array), convert it to grayscale (2D array)."
    if len(arr.shape) == 3:
        return average(arr, -1)  # average over the last axis (color channels)
    else:
        return arr


def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

if __name__ == "__main__":
    main()
