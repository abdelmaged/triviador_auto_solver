#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import gtk.gdk
import datetime
import os
from PIL import Image
import shelve
import blockhash
from evdev import InputDevice, categorize, ecodes
from select import select
import cv2
from subprocess import call
import uinput
import re

data_dir = "../data"
path = os.path.join(data_dir, "search")
path_fix = os.path.join(data_dir, "fix")
path_ans = os.path.join(data_dir, "ans")
path_math = os.path.join(data_dir, "math")
tmp = os.path.join(data_dir, "tmp")
db = shelve.open(os.path.join(data_dir, "dbbin.shelve"))
mont = True  # monitor?

# Init evdev
dev = InputDevice('/dev/input/event2')
print(dev)

# Init uinput
k = {
    "0": uinput.KEY_0, "1": uinput.KEY_1,
    "2": uinput.KEY_2, "3": uinput.KEY_3,
    "4": uinput.KEY_4, "5": uinput.KEY_5,
    "6": uinput.KEY_6, "7": uinput.KEY_7,
    "8": uinput.KEY_8, "9": uinput.KEY_9
}

events = (
    uinput.KEY_0, uinput.KEY_1, uinput.KEY_2, uinput.KEY_3,
    uinput.KEY_4, uinput.KEY_5, uinput.KEY_6, uinput.KEY_7,
    uinput.KEY_8, uinput.KEY_9,
    uinput.KEY_ENTER,
)

device = uinput.Device(events)


def timeStamped(fname, fmt='%d-%m-%Y %H-%M-%S'):
    return datetime.datetime.now().strftime(fmt).format()


# Using uinput
# Write ans in Game answerBox and hit Enter
def putAns(ans):
    cnt = 0
    for c in ans:
        if(c.isdigit()):
            device.emit_click(k[c])
            cnt = cnt + 1
    if cnt == len(ans):
        device.emit_click(uinput.KEY_ENTER)
    return cnt == len(ans)


# Using OpenCV
def binCrop(fname):
    im = cv2.imread(path + fname)

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  # grayscale
    _, thresh = cv2.threshold(
        gray, 150, 255, cv2.THRESH_BINARY_INV)  # threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    dilated = cv2.dilate(thresh, kernel, iterations=13)  # dilate
    contours, hierarchy = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # get contours

    # for each contour found, draw a rectangle around it on original image
    a, b, c, d, q = 0, 0, 0, 1000, 0
    for contour in contours:
        # get rectangle bounding contour
        [x, y, w, h] = cv2.boundingRect(contour)

        # discard areas that are too small
        if h < 40 or w < 40:
            continue

        if(h < d):
            a, b, c, d = x + q, y + q, w - q, h - q

    # write original image with added contours to disk
    os.remove(path + fname)
    # os.rename(path + fname, path + fname + "_")
    if(d != 1000):
        cv2.imwrite(path + fname, thresh[b:b + d, a:a + c])
        return True
    else:
        return False


# Using gtk.gdk
def captureQuestion():
    w = gtk.gdk.get_default_root_window()
    sz = (700, 80)
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(
        w, w.get_colormap(), 255, 335, 0, 0, sz[0], sz[1])
    if (pb is not None):
        fname = timeStamped(".png") + '.png'
        pb.save(path + fname, "png")
        return fname
    return None


# Using gtk.gdk
def captureAnswer(fname):
    w = gtk.gdk.get_default_root_window()
    sz = (700, 300)
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(
        w, w.get_colormap(), 255, 335, 0, 0, sz[0], sz[1])
    if (pb is not None):
        fnameans = fname + "_ans"
        pb.save(path_ans + fnameans, "png")
        # call([
        #     "convert", path_ans + fnameans,
        #     "-quality", "75", path_ans + fnameans + ".jpg"
        # ])
        # os.rename(path_ans + fnameans + ".jpg", path_ans + fnameans)

        print "Answer Saved!.\n"
        return True
    return False


# Using Blockhash module
# Crop BW Image
# Get Image Hash
# Search By imageHash in the shelve DB
def searchAnswer(fname):
    # print "a", datetime.datetime.now() - a
    if(binCrop(fname) == False):
        return False

    im = Image.open(path + fname)
    # print "a", datetime.datetime.now() - a

    if im.mode == '1' or im.mode == 'L' or im.mode == 'P':
        im = im.convert('RGB')
    elif im.mode == 'LA':
        im = im.convert('RGBA')

    h = str(blockhash.blockhash(im, 16))
    # print "a", datetime.datetime.now() - a
    try:
        putted = putAns(db[h][1])
        print "a", datetime.datetime.now() - a

        data = db[h]
        filename = data[0]
        ansy = data[1]

        print filename
        print "***   ", ansy, "   ***"

        image = Image.open(path_ans + filename + "_ans")
        image.show()
        # img = cv2.imread(path_ans + filename + "_ans")
        # cv2.imshow("Saved Answer!", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        if putted is True:
            os.remove(path + fname)
        else:
            os.rename(path + fname, path_fix + fname)
        return True
    except:
        print "NOT FOUND\n"
        return False


# Using evdev
# Check for hotkey(`) is pressed
def getkey(who):
    while True:
        r, w, x = select([dev], [], [])
        for event in dev.read():
            if event.type == ecodes.EV_KEY:
                # timestamp , scancode, keycode, keystate
                s = categorize(event)
                if((s.keycode == 'KEY_GRAVE' and s.keystate == 1) and
                   (mont is True or who == 1)):
                    return True
                else:
                    return False


# train
# gocr -p ../db/ -m 386 -a 100 output-4.png
# gocr -i 1.png -C 0123456789 -m 386 -p ./db/
# perform ocr
# gocr -p ../db/ -m 258 output-4.png
# gocr -i 1.png -C 0123456789 -m 258 -p ./db/
def predictMath(fname):
    # call(["tesseract", "-psm", "7", path + fname, tmp + "out"])
    call(["gocr", "-i", path + fname, "-o", tmp + "out",
          "-C", "0123456789/*+~", "-m", "258", "-p", "./db/"])
    content = ""
    with open(tmp + 'out', 'r') as content_file:
        content = content_file.read().strip()

    os.remove(tmp + 'out')
    numbers = map(int, re.findall(r"[\d']+", content))
    op = re.findall(r"[/*+~']+", content)

    if(len(op) == 1 and len(numbers) == 2):
        eq = -1
        if(op[0] == "*"):
            eq = numbers[1] * numbers[0]
        elif(op[0] == "/" and numbers[0] != 0):
            eq = numbers[1] / numbers[0]
        elif(op[0] == "+"):
            eq = numbers[1] + numbers[0]
        elif(op[0] == "~"):
            eq = numbers[0] - numbers[1]
        putAns(str(eq))
        print numbers[1], op[0], numbers[0], "=", eq
        os.remove(path + fname)
        return True
    return False

# Main
a = datetime.datetime.now()
while True:
    print "<Q>..."
    if(getkey(0) == True):
        a = datetime.datetime.now()
        mont = False
        fname = captureQuestion()
        if(fname is not None and searchAnswer(fname) == False):
            if predictMath(fname) == True:
                mont = True
                continue
            print "(A)."
            while True:
                if(getkey(1) == True):
                    captureAnswer(fname)
                    break
        mont = True


# Test Area - ay btngan
# reshaped_text = arabic_reshaper.reshape(u'اللغة العربية رائعة')
# bidi_text = get_display(reshaped_text)
# print bidi_text
