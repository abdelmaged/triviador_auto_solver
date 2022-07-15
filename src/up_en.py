#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
from subprocess import call

path = "/home/abdelmaged/saif/search/"
path_ans = "/home/abdelmaged/saif/ans/"
tmp = "/home/abdelmaged/saif/tmp/"


def ocrAnswer(fname):
    im = Image.open(path_ans + fname)
    # im.show()

    mi = im.crop([440, 211, 630, 250])
    mi.save(tmp + fname + ".png")

    call(["tesseract", "-psm", "6", tmp + fname + ".png",
          tmp + "out", "nobatch", "digits"])
    content = ""
    with open(tmp + 'out.txt', 'r') as content_file:
        content = content_file.read().strip()

    # print content
    os.remove(tmp + 'out.txt')
    # os.remove(tmp + fname + ".png")
    if content.isdigit():
        return content
    else:
        return "!"

if __name__ == '__main__':
    db = shelve.open("./dbbin_en.shelve")
    for fname in os.listdir(path):
        im = Image.open(path + fname)
        if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
            im = im.convert('RGB')
        elif im.mode == 'LA':
            im = im.convert('RGBA')

        h = str(blockhash.blockhash(im, 16))
        print ocrAnswer(fname + "_ans")
        try:
            filenames = db[h]
            print fname, filenames
            print "Found %d images" % (len(filenames))
            # os.remove(path + fname)
        except:
            try:
                ansy = ocrAnswer(fname + "_ans")
                print fname
                print "***   ", ansy, "   ***"
                # db[h] = db.get(h, []) + [fname, ansy]
                # os.rename(path + fname, "./cropped/" + fname)
            except:
                print "NOT FOUND", fname

print "\ndb size: ", len(db)
