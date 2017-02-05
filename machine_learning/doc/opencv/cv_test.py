#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: cv_test.py
@date: 2016-11-16
"""
__author__ = "abc"

import cv2


fn = "/home/abc/Projects/machine_learning/test.jpg"


if __name__ == "__main__":
    img = cv2.imread(fn)

    w = img.shape[1]
    h = img.shape[0]
    ii = 0

    print ''
    for xi in xrange(0, w):
        for xj in xrange(0, h):
            img[xj, xi, 0] = int(img[xj, xi, 0] * 0.2)
            img[xj, xi, 1] = int(img[xj, xi, 1] * 0.2)
            img[xj, xi, 2] = int(img[xj, xi, 2] * 0.2)
        if xi % 10 == 0:
            print '.',

    cv2.namedWindow('img')
    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print ''
    for xi in xrange(0, w):
        for xj in xrange(0, h):
            img[xj, xi, 0] = int(img[xj, xi, 0] * 3.9)
            img[xj, xi, 1] = int(img[xj, xi, 1] * 3.9)
            img[xj, xi, 2] = int(img[xj, xi, 2] * 3.9)
        if xi % 10 == 0:
            print '.',

    cv2.namedWindow('img')
    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    print ''
    for xi in xrange(0, w):
        for xj in xrange(0, h):
            img[xj, xi, 0] = int(img[xj, xi, 0] * 0.7)
            img[xj, xi, 1] = int(img[xj, xi, 1] * 0.7)
        if xi % 10 == 0:
            print '.',

    cv2.namedWindow('img')
    cv2.imshow("img", img)
    cv2.waitKey()
    cv2.destroyAllWindows()
