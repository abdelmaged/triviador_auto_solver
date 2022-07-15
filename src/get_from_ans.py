#! /usr/bin/env python
#

import gtk.gdk
import datetime
import os
from PIL import Image
import shelve
import blockhash
import cv2
from subprocess import call
import uinput
import re

pathss = "/home/abdelmaged/saif/fix_new/"
path_ans = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"
path = "/home/abdelmaged/saif/found/"
path_custom = path + "Screenshot from 2018-03-23 18-29-36.png"

def timeStamped(fname, fmt='%d-%m-%Y %H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format()

# Using OpenCV
def binCrop(fname):
    im = cv2.imread(path + fname)
    crop_img = im[10:100, 10:-30]


    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)  # grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=2)  # dilate
    _, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    # for each contour found, draw a rectangle around it on original image
    xmin, ymin, xmax, ymax = 1000, 1000, 0, 0
    for contour in contours:
      [x, y, w, h] = cv2.boundingRect(contour)

      if(x < xmin):
         xmin = x
      if(x+w > xmax):
         xmax = x+w
      if(y < ymin):
         ymin = y
      if(y+h > ymax):
         ymax = y+h

    a, b, c, d = xmin, ymin, xmax-xmin, ymax-ymin

    # write original image with added contours to disk
    # os.rename(path + fname, path + fname + "test")
    if(d != 1000):
        cv2.imwrite(path + fname[:-4], thresh[b:b + d, a:a + c])
        return True
    else:
        return False


if __name__ == '__main__':
   for fname in sorted(os.listdir(path)):
      binCrop(fname)
   #binCrop("21-10-2015 00-27-57.png")
   #binCrop("24-03-2018 00-22-48.png")


   





