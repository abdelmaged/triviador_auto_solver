#! /usr/bin/env python
#

import PIL.Image as Image
import os
import shelve
import blockhash
import shutil
from subprocess import call

path = "/home/abdelmaged/saif/search/"
path_found = "/home/abdelmaged/saif/found/"
path_cropped = "/home/abdelmaged/saif/cropped/"
path_ans = "/home/abdelmaged/saif/ans/"
tmp = "/home/abdelmaged/saif/tmp/"
val = "2003"


if __name__ == '__main__':
    db = shelve.open("./dbbin.shelve")
    for record in db:
        record = db.get(record, [])
        if record[1] == val:
            print record
            im = Image.open(path_cropped + record[0])
            # im.show()
            shutil.copy(path_cropped + record[0], path_found + record[0])

print "\ndb size: ", len(db)
