#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: cv_test3.py
@date: 2016-11-17
"""
__author__ = "abc"

import cv2
import numpy as np

fn = "/home/abc/Projects/machine_learning/test.jpg"
fn2 = "/home/abc/Projects/machine_learning/test2.jpg"

if __name__ == "__main__":
    img = cv2.imread(fn)
    img2 = cv2.imread(fn2)

    sz0 = img.shape[0]
    sz1 = img.shape[1]
    for y in xrange(0, sz0):
        for x in xrange(0, sz1):
            img2[y, x, :] = img[y, x, :] * 0.5 + img2[y, x, :] * 0.5
        print ".",

    cv2.namedWindow('img')
    cv2.imshow("img", img2)
    cv2.waitKey()
    cv2.destroyAllWindows()
