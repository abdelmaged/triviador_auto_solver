#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
from subprocess import call

path = "/home/abdelmaged/saif/fix_2018/"
path_ans = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"
path_ori = "/home/abdelmaged/saif/cropped_2018/"
path_custom = path_ori + "17-06-2015 17-18-17.png"


def ocrAnswer(fname):
    im = Image.open(path_ans + fname)
    # im.show()

    #mi = im.crop([440, 210, 630, 250])
    mi = im.crop([190, 110, 440, 165])
    mi.save(tmp + fname + ".png")
#    mi.show()

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

# 9-7, 2,45,40
if __name__ == '__main__':
    db = shelve.open("./dbbin_2018_22.shelve")
    slist = sorted(os.listdir(path))
    # slist = ["test"]
    a = 0
    for fname in slist:
        a = a + 1
        # if(a > 2):
        #     break
        im = Image.open(path + fname)
        # im = Image.open(path_custom)
        if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
            im = im.convert('RGB')
        elif im.mode == 'LA':
            im = im.convert('RGBA')

        h = str(blockhash.blockhash(im, 22))
        print h
        try:
            filename = db[h]
            # im = Image.open(path_ori + filename[0])
            im = Image.open(path_ans + filename[0] + "_ans")
            im.show()
            ansOcr = ocrAnswer(filename[0] + "_ans")
            print "OCR: ***", ansOcr, "***"
            print fname, filename
            # print "Found %d images" % (len(filename)/2)
            msg = "(Y)es Correct OCR Answer\n(D)elete image\n"
            msg += "(DB) delete from database\nElse Enter Answer ?"
            decision = raw_input(msg)
            if(decision == "y"):
                db[h] = [filename[0], ansOcr]
            elif(decision == "d"):
                os.remove(path + fname)
            elif(decision == "db"):
                del db[h]
            else:
                db[h] = [filename[0], decision]
        except:
            print "not found"
        print "\n"

print "\ndb size: ", len(db)
