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


def ocrAnswer(fname):
    im = Image.open(path_ans + fname)
    # im.show()

#    mi = im.crop([190, 130, 445, 185])
    mi = im.crop([190, 110, 440, 165])
    mi.save(tmp + fname + ".png")

    call(["tesseract", "-psm", "6", tmp + fname + ".png",
          tmp + "out", "nobatch", "digits"])
    content = ""
    with open(tmp + 'out.txt', 'r') as content_file:
        content = content_file.read().strip()

    # print content
    os.remove(tmp + 'out.txt')
    #os.remove(tmp + fname + ".png")
    if content.isdigit():
        return content
    else:
        return "!"

if __name__ == '__main__':

    c = 0
    for fname in sorted(os.listdir(path)):
      im = Image.open(path + fname)
      width, height = im.size
      if height > 70:
         c = c+1
         print fname, width, height
         copyfile(path + fname, tmp + fname)
         #os.rename(path + fname, tmp + fname)
    print c

   #print ocrAnswer("24-03-2018 01-18-12.png_ans")


