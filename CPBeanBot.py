from PIL import ImageGrab
import pynput.mouse as ms
from pynput.mouse import Listener
import cv2 as cv
import numpy as np
import glob

# match template choices
# cv.TM_CCOEFF.........maybe
# cv.TM_CCOEFF_NORMED..good
# cv.TM_CCORR..........not good
# cv.TM_CCORR_NORMED...8
# cv.TM_SQDIFF.........not good
# cv.TM_SQDIFF_NORMED..

mt = cv.TM_SQDIFF_NORMED

# imread choices
# cv.IMREAD_UNCHANGED
# cv.IMREAD_GRAYSCALE
# cv.IMREAD_COLOR
# cv.IMREAD_ANYDEPTH

ir = cv.IMREAD_UNCHANGED

mouse = ms.Controller()

need = glob.glob("C:\\Users\\kille\\Desktop\\image finder\\bean game\\bb_img\\*.png")

needle_w = needle.shape[1]
needle_h = needle.shape[0]

result = cv.matchTemplate(haystack, needle, mt)


def mouseClick():
    mouse.press(ms.Button.left)
    mouse.release(ms.Button.left)


def newPic():
    global screen
    screen = np.array(ImageGrab.grab())
    screen = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)

    # result = cv.matchTemplate(screen, best(), mt)
    # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)


def dropOff():
    mouse.position = (400, 828)
    mouseClick()
    mouseClick()
    mouseClick()


def best():
    bestVal = .001
    best_match = None
    newPic()
    for bag in need:
        needle = cv.imread(bag, ir)
        result = cv.matchTemplate(screen, needle, mt)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        threshold = .2
        if max_val <= threshold:
            if max_val > bestVal:
                bestVal = max_val
                best_match = bag
            # print('Conf: ' + str(max_val))
    if best_match is not None:
        needle = cv.imread(str(best_match), ir)
        print('The highest confidence was: ' + str(bestVal))
        print('The best match would be: ' + str(best_match))
        result = cv.matchTemplate(screen, needle, mt)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        needle_w = needle.shape[1]
        needle_h = needle.shape[0]
        top_left = max_loc
        center = (top_left[0] + (needle_w / 2), top_left[1] + (needle_h / 2))
        bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
        # mouse.position = center
        # cv.rectangle(screen, top_left, bottom_right, color=(255, 0, 0), thickness=2, lineType=cv.LINE_4)
        # cv.imshow('Result', screen)
        # cv.waitKey(2000)
        # cv.destroyWindow('Result')
    else:
        print('Nothing was found')


screen = np.array(ImageGrab.grab())
screen = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)

for y in range(50):
    for x in range(2):
        best()
    dropOff()
