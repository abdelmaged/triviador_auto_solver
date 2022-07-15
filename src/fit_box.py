#! /usr/bin/env python
#

import gtk.gdk
import datetime
import os
from PIL import Image
import shelve
import blockhash
from evdev import InputDevice, categorize, ecodes
from select import select
import cv2
from subprocess import call
import uinput
import re

pathss = "/home/abdelmaged/saif/fix_new/"
path_ans = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"
path = "/home/abdelmaged/saif/search_2018/"
path_custom = path + "Screenshot from 2018-03-23 18-29-36.png"

def timeStamped(fname, fmt='%d-%m-%Y %H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format()


def captureQuestion():
    w = gtk.gdk.get_default_root_window()
    sz = (580, 85)
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(
        w, w.get_colormap(), 220, 195, 0, 0, sz[0], sz[1])
    if (pb is not None):
        fname = timeStamped(".png") + '.png'
        pb.save(path + fname, "png")
        return fname
    return None

# Using OpenCV
def binCrop(fname):
    im = cv2.imread(path + fname)
    fname = "BW" + fname
    f2 = "CNT" + fname

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # grayscale

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=2)  # dilate
    #closed  = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  #Does the trick
    
    _, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    #cv2.imwrite(path + f2, closed)

    # for each contour found, draw a rectangle around it on original image
    xmin, ymin, xmax, ymax = 1000, 1000, 0, 0
    for contour in contours:
      [x, y, w, h] = cv2.boundingRect(contour)
      #cv2.rectangle(thresh,(x,y),(x+w,y+h),(255,255,255),1)
      print x, y, w, h

      if(x < xmin):
         xmin = x
      if(x+w > xmax):
         xmax = x+w
      if(y < ymin):
         ymin = y
      if(y+h > ymax):
         ymax = y+h

    a, b, c, d = xmin, ymin, xmax-xmin, ymax-ymin

    print len(contours)
    #cv2.drawContours(thresh, contours,-1,(255,255,255),1)
    #cv2.rectangle(thresh,(a,b),(a+c,b+d),(255,255,255),1)
    h, w, _ = im.shape
    #cv2.rectangle(thresh,(0,0),(w-1,h-1),(255,255,255),1)

    #cv2.imwrite(path + f2, thresh)

    print "\n"
    print a,b,c,d
    # write original image with added contours to disk
    # os.rename(path + fname, path + fname + "test")
    if(d != 1000):
        cv2.imwrite(path + fname, thresh[b:b + d, a:a + c])
        return True
    else:
        return False


if __name__ == '__main__':
   #captureQuestion()
   binCrop(captureQuestion())
   #binCrop("21-10-2015 00-27-57.png")
   #binCrop("24-03-2018 00-22-48.png")


   





