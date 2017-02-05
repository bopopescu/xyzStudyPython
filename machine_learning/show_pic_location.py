#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: euclidean_distance.py
@date: 2016-12-09
@desc: 差分矩阵求和/均值
"""
__author__ = "abc"

import cv2
import numpy as np


def show_pic_location(img, findimg):
    """
    show_pic_location
    :param img:
    :param findimg:
    :return:
    """
    w = img.shape[1]
    h = img.shape[0]
    fw = findimg.shape[1]
    fh = findimg.shape[0]
    findpt = None
    for now_h in xrange(h - fh):
        for now_w in xrange(w - fw):
            comp_tz = img[now_h:now_h + fh, now_w: now_w + fw, :] - findimg
            # 求和
            # if np.sum(comp_tz) < 1:
            #     findpt = now_w, now_h
            # 均值
            if abs(np.mean(comp_tz)) < 20:
                findpt = now_w, now_h
    if findpt is not None:
        cv2.rectangle(img, findpt, (findpt[0] + fw, findpt[1] + fh), (255, 0, 0))
    return img


def add_noise(img):
    """
    add_noise
    :param img:
    :return:
    """
    count = 30000
    for k in xrange(count):
        xi = int(np.random.uniform(0, img.shape[1]))
        xj = int(np.random.uniform(0, img.shape[0]))
        img[xj, xi, 0] = 255 * np.random.rand()
        img[xj, xi, 1] = 255 * np.random.rand()
        img[xj, xi, 2] = 255 * np.random.rand()


def handle_img(imgpath, imgpath1, imgpath2):
    """
    handle_img
    :param imgpath:
    :param imgpath1:
    :param imgpath2:
    :return:
    """
    myimg = cv2.imread(imgpath)
    myimg1 = cv2.imread(imgpath1)
    myimg2 = cv2.imread(imgpath2)

    cv2.namedWindow('img1')
    cv2.imshow('img1', myimg1)
    cv2.namedWindow('img2')
    cv2.imshow('img2', myimg2)

    cv2.waitKey()
    cv2.destroyAllWindows()



    add_noise(myimg)

    myimg = show_pic_location(myimg, myimg1)
    myimg = show_pic_location(myimg, myimg2)

    cv2.namedWindow('img')
    cv2.imshow('img', myimg)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    imgpath = "/home/abc/Projects/machine_learning/img/test.png"
    imgpath1 = "/home/abc/Projects/machine_learning/img/test_1.png"
    imgpath2 = "/home/abc/Projects/machine_learning/img/test_2.png"
    handle_img(imgpath, imgpath1, imgpath2)
