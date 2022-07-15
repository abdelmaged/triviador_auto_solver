#! /usr/bin/env python
#

import os
import re
import math
from subprocess import call

path = "/home/abdelmaged/saif/math/"
path_ans = "/home/abdelmaged/saif/ans/"
tmp = "/home/abdelmaged/saif/tmp/"


def swap(s, i, j):
    return ''.join((s[:i], s[j], s[i + 1:j], s[i], s[j + 1:]))

# train
# gocr -p ../db/ -m 386 -a 100 output-4.png
# gocr -i ./math/1.png -C "0123456789/*+~.$&@" -m 386 -p ./db/
# perform ocr
# gocr -p ../db/ -m 258 output-4.png
# gocr -i 1.png -C 0123456789 -m 258 -p ./db/


def swOp(op, n0, n1):
   eq = -1
   if(op == "*"):
      eq = n1 * n0
   elif(op == "/" and n0 != 0):
      eq = n1 / n0
   elif(op == "+"):
      eq = n1 + n0
   elif(op == "~"):
      eq = n0 - n1
   elif(op == "$"): # percentage
      eq = n0*n1/100
   elif(op == "&"):
      eq = int(math.sqrt(n0))
   elif(op == "@"):
      eq = n0+n0
   return eq

def predictMath(fname):
    # call(["tesseract", "-psm", "7", path + fname, tmp + "out"])
    call(["gocr", "-i", path + fname, "-o", tmp + "out",
          "-C", "0123456789/*+~.$&@", "-m", "258", "-p", "./db/"])
    content = ""
    with open(tmp + 'out', 'r') as content_file:
        content = content_file.read().strip()

    print content
    i = 0
    sz = len(content)
    while i < sz:
        if(content[i - 1].isdigit()
            and content[i] == '.'
            and content[i + 1].isdigit()):
            content = swap(content, i - 1, i)
            i = i - 1
            print content
        else:
            i = i+1

    os.remove(tmp + 'out')
    numbers = map(int, re.findall(r"[\d']+", content))
    op = re.findall(r"[/*+~$&@']+", content)
    print op, numbers
    if(len(op) == 1 and len(numbers) == 2):
        eq = swOp(op[0], numbers[0], numbers[1])
        print numbers[1], op[0], numbers[0], "=", eq
        return True
    elif(len(op) == 2 and len(numbers) == 3):
        eq = swOp(op[1], numbers[2], numbers[1])
        eq = swOp(op[0], eq, numbers[0])
        print numbers[2], op[1], numbers[1], op[0], numbers[0], "=", eq
        return True
    elif(len(op) == 3 and len(numbers) == 4):
        eq = swOp(op[2], numbers[3], numbers[2])
        eq = swOp(op[1], eq, numbers[1])
        eq = swOp(op[0], eq, numbers[0])
        print numbers[3], op[2], numbers[2], op[1], numbers[1], op[0], numbers[0], "=", eq
        return True
    elif(len(op) == 1 and len(numbers) == 1):
        eq = swOp(op[0], numbers[0], 0)
        print op[0], numbers[0], "=", eq
        return True
      
   
    return False

# 9-7, 2,45,40
if __name__ == '__main__':
    l = sorted(os.listdir(path))
    for fname in l:
        print predictMath(fname), fname
