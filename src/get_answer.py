#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
from subprocess import call
from shutil import copyfile



pathss = "/home/abdelmaged/saif/fix_new/"
path_ans = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"
path = "/home/abdelmaged/saif/cropped_2018/"
path_custom = path + "17-06-2015 17-18-17.png"


if __name__ == '__main__':
    db = shelve.open("./dbbin_2018.shelve")
    for v, k in db.items():
      if k[1] == '525':
         im = Image.open(path_ans + k[0] + "_ans")
         #im.show()
         print v, k
         copyfile(path + k[0], tmp + k[0])
         copyfile(path_ans + k[0] + "_ans", tmp + k[0] + "_ans")

print "\ndb size: ", len(db)
