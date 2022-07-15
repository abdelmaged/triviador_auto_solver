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
import shelve
import blockhash

pathss = "/home/abdelmaged/saif/fix_new/"
path_ans = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"
path_cropped_old = "/home/abdelmaged/saif/cropped_old/"
path_cropped_new = "/home/abdelmaged/saif/cropped_old_2/"
path = tmp

def timeStamped(fname, fmt='%d-%m-%Y %H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format()


# Using OpenCV
def binCrop(fname):
    im = cv2.imread(path_cropped_old + fname)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # grayscale

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # threshold

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
        cv2.imwrite(path_cropped_new + fname, thresh[b:b + d, a:a + c])
        return True
    else:
        return False


if __name__ == '__main__':
   #captureQuestion()
   #binCrop(captureQuestion())
   #binCrop("21-10-2015 00-27-57.png")
   #binCrop("23-03-2018 19-02-03.png")


   db_2018 = shelve.open("./dbbin_2018.shelve")
   #db = shelve.open("./dbbin_new.shelve")
   
   for fname in sorted(os.listdir(path_cropped_old)):
      #binCrop(fname)
      
      if(binCrop(fname)):
         im = Image.open(path_cropped_new + fname)
         if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
            im = im.convert('RGB')
         elif im.mode == 'LA':
            im = im.convert('RGBA')
         h = str(blockhash.blockhash(im, 16))

         for v, k in db_2018.items():
            if(k[0] == fname):
               db_2018[h] = db_2018.get(h, []) + k
               break
      
   #print "\ndb size: ", len(db_2018)
   #print "\ndb size: ", len(db)



   





