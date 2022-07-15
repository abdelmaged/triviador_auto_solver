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
tmp = "/home/abdelmaged/saif/found/"
path = "/home/abdelmaged/saif/cropped_2018/"
path_custom = path + "17-06-2015 17-18-17.png"


def getHash(fpath, bit):
    im = Image.open(fpath)
    if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
        im = im.convert('RGB')
    elif im.mode == 'LA':
        im = im.convert('RGBA')

    return str(blockhash.blockhash(im, bit))


if __name__ == '__main__':


   db_2018 = shelve.open("./dbbin_2018.shelve")
   db = shelve.open("./dbbin_2018_24.shelve")
   
   
   for fname in sorted(os.listdir(path)):
      h_13 = getHash(path + fname, 24)
      h_16 = getHash(path + fname, 16)
      try:
         record = db[h_13]
         print record
         copyfile(path + fname, tmp + h_13 + fname)
         copyfile(path + record[0], tmp + h_13 + record[0])
      except:
         db[h_13] = db_2018[h_16]
   

   print len(db_2018)
   print len(db)

