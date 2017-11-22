#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: euclidean_distance.py
@date: 2016-12-09
@desc: 余弦相似度
"""
__author__ = "abc"

import cv2
import numpy as np

w_fg = 20
h_fg = 15
pic_flag = 3


def read_pic(fn):
    """
    read_pic
    :param fn:
    :return:
    """
    fnimg = cv2.imread(fn)
    img = cv2.resize(fnimg, (800, 600), interpolation=cv2.INTER_AREA)
    w = img.shape[1]
    h = img.shape[0]
    w_interval = w / w_fg
    h_interval = h / h_fg

    alltz = []
    alltz.append([])
    alltz.append([])
    alltz.append([])

    for now_h in xrange(0, h, h_interval):
        for now_w in xrange(0, w, w_interval):
            b = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 0]
            g = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 1]
            r = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 2]
            btz = np.mean(b)
            gtz = np.mean(g)
            rtz = np.mean(r)

            alltz[0].append(btz)
            alltz[1].append(gtz)
            alltz[2].append(rtz)

    return alltz


def get_cossimi(x, y):
    """
    get_cossimi
    :param x:
    :param y:
    :return:
    """
    myx = np.array(x)
    myy = np.array(y)
    cos1 = np.sum(myx * myy)
    cos21 = np.sqrt(sum(myx * myx))
    cos22 = np.sqrt(sum(myy * myy))
    return cos1 / float(cos21 * cos22)


if __name__ == "__main__":
    # 提取特征
    train_x = []
    d = []

    for ii in xrange(1, pic_flag + 1):
        smp_x = []
        b_tz = np.array([0, 0, 0])
        g_tz = np.array([0, 0, 0])
        r_tz = np.array([0, 0, 0])
        mytz = np.zeros((3, w_fg * h_fg))
        for jj in xrange(1, 3):
            fn = '/home/abc/Projects/machine_learning/img/base/p' + str(ii) + '-' + str(jj) + '.jpg'
            print fn
            tmptz = read_pic(fn)
            mytz += np.array(tmptz)
        mytz /= 3
        train_x.append(mytz[0].tolist() + mytz[1].tolist() + mytz[2].tolist())

    for index in xrange(1, 5):
        fn = '/home/abc/Projects/machine_learning/img/base/test{}.jpg'.format(index)
        testtz = np.array(read_pic(fn))
        simtz = testtz[0].tolist() + testtz[1].tolist() + testtz[2].tolist()
        maxtz = 0
        nowi = 0

        for i in xrange(pic_flag):
            nowsim = get_cossimi(train_x[i], simtz)
            if nowsim > maxtz:
                maxtz = nowsim
                nowi = i

        print '%s属于第%d类' % (fn, nowi + 1)
