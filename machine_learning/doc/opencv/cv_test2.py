#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: cv_test2.py
@date: 2016-11-17
"""
__author__ = "abc"

import numpy as np
import cv2


if __name__ == "__main__":
    sz1 = 600
    sz2 = 800

    img = np.zeros((sz1, sz2, 3), np.uint8)
    pos1 = np.random.randint(sz1, size=(2000, 1))
    pos2 = np.random.randint(sz2, size=(2000, 1))

    for i in range(2000):
        img[pos1[i], pos2[i], [0]] = np.random.randint(0, 255)
        img[pos1[i], pos2[i], [1]] = np.random.randint(0, 255)
        img[pos1[i], pos2[i], [2]] = np.random.randint(0, 255)

    print img.shape

    cv2.imshow('prev', img)

    cv2.waitKey()

    cv2.destroyAllWindows()
