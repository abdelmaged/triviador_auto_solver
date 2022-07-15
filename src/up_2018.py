#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
from subprocess import call

path = "/home/abdelmaged/saif/search_2018/"
path_ans = "/home/abdelmaged/saif/ans_new/"
path_cropped = "/home/abdelmaged/saif/cropped_2018/"
tmp = "/home/abdelmaged/saif/tmp/"


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
    os.remove(tmp + fname + ".png")
    if content.isdigit():
        return content
    else:
        return "!"

if __name__ == '__main__':
    db = shelve.open("./dbbin_2018_23.shelve")
    for fname in sorted(os.listdir(path)):
        fnameans = fname + "_ans"
        im = Image.open(path + fname)
        if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
            im = im.convert('RGB')
        elif im.mode == 'LA':
            im = im.convert('RGBA')

        h = str(blockhash.blockhash(im, 23))
        try:
            filenames = db[h]
            print fname, filenames
            print "Found %d images" % (len(filenames))
            asf = Image.open(path_ans + filenames[0] + "_ans")
            asf.show()
            # os.remove(path + fname)
        except:
            try:
                ansy = ocrAnswer(fname + "_ans")
                print fname
                print "***   ", ansy, "   ***"
                call([
                    "convert", path_ans + fname + "_ans",
                    "-quality", "10", path_ans + fname + "_ans.jpg"
                ])
                os.rename(path_ans + fnameans + ".jpg", path_ans + fnameans)
                db[h] = db.get(h, []) + [fname, ansy]
                os.rename(path + fname, path_cropped + fname)
            except:
                print "NOT FOUND", fname

print "\ndb size: ", len(db)
