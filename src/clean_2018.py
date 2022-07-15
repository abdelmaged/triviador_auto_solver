#! /usr/bin/env python
#

import os
import shelve
import PIL.Image as Image
import blockhash

path = "/home/abdelmaged/saif/search_2018/"
path_found = "/home/abdelmaged/saif/found/"
path_cropped = "/home/abdelmaged/saif/cropped_2018/"
path_ans = "/home/abdelmaged/saif/ans_new/"
path_cropped_new = "/home/abdelmaged/saif/cropped_2018/"
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

    db = shelve.open("./dbbin_2018.shelve")
    print "db_NEW size: ", len(db), "\n"

    lost = 0
    dic = {}
    for h in db:
        record = db.get(h, [])
        filename = record[0]
        dic[filename] = 1
        if(not os.path.exists(path_ans_new + filename + "_ans")):
            lost = lost + 1
            del db[h]

    print "In DB            BUT NOT in AnswerFolder  : ", lost

    for h in db:
        record = db.get(h, [])
        i = 0
        while(i < len(record)):
         filename = record[i]
         if(not os.path.exists(path_cropped_new + filename)):
               print record
               lost = lost + 1
         i = i + 2
    print "In DB            BUT NOT in CroppedFolder : ", lost

    lost = 0
    for fname in os.listdir(path_ans_new):
       if(not dic.has_key(fname[:-4])):
         lost = lost + 1
         os.rename(path_ans_new + fname, path_found + fname)
    print "In AnswerFolder  BUT NOT in DB            : ", lost

    '''
    lost = 0
    for fname in os.listdir(path_cropped_new):
      h = getHash(path_cropped_new + fname)
      try:
         record = db[h]
      except:
         lost = lost + 1
         os.rename(path_cropped_new + fname, path_found + fname)

    print "In CroppedFolder BUT NOT in DB            : ", lost
    '''

    lost = 0
    for fname in os.listdir(path_cropped_new):
        found = not os.path.exists(path_ans_new + fname + "_ans")
        if(found):
            lost = lost + 1
            os.rename(path_cropped_new + fname, path_found + fname)

    print "In CroppedFolder BUT NOT in AnswerFolder  : ", lost


    lost = 0
    for fname in os.listdir(path_ans_new):
        if(not os.path.exists(path_cropped_new + fname[:-4])):
            lost = lost + 1
            os.rename(path_ans_new + fname, path_found + fname)

    print "In AnswerFolder  BUT NOT in CroppedFolder : ", lost
