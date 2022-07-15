#! /usr/bin/env python
#

import os
import shelve
import PIL.Image as Image
import blockhash

path = "/home/abdelmaged/saif/search/"
path_found = "/home/abdelmaged/saif/found/"
path_cropped = "/home/abdelmaged/saif/cropped/"
path_ans = "/home/abdelmaged/saif/ans/"
path_cropped_new = "/home/abdelmaged/saif/cropped_new/"
path_ans_new = "/home/abdelmaged/saif/ans_new/"
tmp = "/home/abdelmaged/saif/tmp/"


def getHash(fpath):
    im = Image.open(fpath)
    if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
        im = im.convert('RGB')
    elif im.mode == 'LA':
        im = im.convert('RGBA')

    return str(blockhash.blockhash(im, 16))

if __name__ == '__main__':
    # in db and not img folders
    db = shelve.open("./dbbin.shelve")
    lost = 0
    for h in db:
        record = db.get(h, [])
        filename = record[0]
        if(not os.path.exists(path_ans + filename + "_ans") or
                not os.path.exists(path_cropped + filename)):
            lost = lost + 1

    print "Not Found in DB: ", lost
    print "db_NEW size: ", len(db)

    db = shelve.open("./dbbin_new.shelve")
    lost = 0
    for record in db:
        record = db.get(record, [])
        filename = record[0]
        if(not os.path.exists(path_ans_new + filename + "_ans")):
            lost = lost + 1

    print "Not Found in DB_NEW: ", lost
    print "db_NEW size: ", len(db), "\n"

    db = shelve.open("./dbbin.shelve")
    lost = 0
    for fname in os.listdir(path_cropped):
        found = not os.path.exists(path_ans + fname + "_ans")
        # if(not found):
        #     h = getHash(path_cropped + fname)
        #     try:
        #         record = db[h]
        #         found = record[0] != fname
        #     except:
        #         found = True
        if(found):
            lost = lost + 1
            os.rename(path_cropped + fname, path_found + fname)

    print "Not Found in Cropped Folder: ", lost

    db = shelve.open("./dbbin_new.shelve")
    lost = 0
    for fname in os.listdir(path_cropped_new):
        found = not os.path.exists(path_ans_new + fname + "_ans")
        # if(not found):
        #     h = getHash(path_cropped_new + fname)
        #     try:
        #         record = db[h]
        #         found = record[0] != fname
        #     except:
        #         found = True
        if(found):
            lost = lost + 1
            os.rename(path_cropped_new + fname, path_found + fname)

    print "Not Found in Cropped_NEW Folder: ", lost, "\n"

    lost = 0
    for fname in os.listdir(path_ans):
        if(not os.path.exists(path_cropped + fname[:-4])):
            lost = lost + 1
            os.rename(path_ans + fname, path_found + fname)

    print "Not Found in Answer Folder: ", lost

    lost = 0
    for fname in os.listdir(path_ans_new):
        if(not os.path.exists(path_cropped_new + fname[:-4])):
            lost = lost + 1
            os.rename(path_ans_new + fname, path_found + fname)

    print "Not Found in Answer_NEW Folder: ", lost, "\n"
