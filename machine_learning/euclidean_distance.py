#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: euclidean_distance.py
@date: 2016-12-09
@desc: 欧氏距离
"""
__author__ = "abc"

import cv2
import numpy as np


def get_euclidean_distance(x, y):
    """
    计算欧氏距离
    :param x:
    :param y:
    :return:
    """
    myx = np.array(x)
    myy = np.array(y)
    return np.sqrt(np.sum((myx - myy) * (myx - myy)))


def handle_img(imgpath):
    """
    handle_img
    :param imgpath:
    :return:
    """
    myimg1 = cv2.imread(imgpath)

    cv2.namedWindow('img1')
    cv2.imshow('img1', myimg1)
    cv2.waitKey()
    cv2.destroyAllWindows()

    w = myimg1.shape[1]
    h = myimg1.shape[0]

    sz1 = w
    sz0 = h

    flag = 16

    myimg2 = np.zeros((sz0, sz1, 3), np.uint8)
    black = np.array([0, 0, 0])
    white = np.array([255, 255, 255])
    centercolor = np.array([125, 125, 125])
    for y in xrange(sz0 - 1):
        for x in xrange(sz1 - 1):
            myhere = myimg1[y, x, :]
            mydown = myimg1[y + 1, x, :]
            myright = myimg1[y, x + 1, :]

            lmyhere = myhere
            lmyright = myright
            lmydown = mydown

            if get_euclidean_distance(lmyhere, lmydown) > flag and get_euclidean_distance(lmyhere, lmyright) > flag:
                myimg2[y, x, :] = black
            elif get_euclidean_distance(lmyhere, lmydown) <= flag and get_euclidean_distance(lmyhere, lmyright) <= flag:
                myimg2[y, x, :] = white
            else:
                myimg2[y, x, :] = centercolor

    cv2.namedWindow('img2')
    cv2.imshow('img2', myimg2)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    imgpath = "/home/abc/Projects/machine_learning/img/test4.png"
    handle_img(imgpath)
