#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: euclidean_distance.py
@date: 2016-12-09
@desc: pca图像特征提取
"""

__author__ = "abc"

import cv2
import mlpy
import numpy as np
import pylab as pl
import neurolab as nl

w_fg = 20
h_fg = 10
pic_flag = 3


def get_result(simjg):
    """
    get_result
    :param simjg:
    :return:
    """
    jg = []
    for j in xrange(len(simjg)):
        maxjg = -2
        nowii = 0
        for i in xrange(len(simjg[0])):
            if simjg[j][i] > maxjg:
                maxjg = simjg[j][i]
                nowii = i
        jg.append(len(simjg[0]) - nowii)
    return jg


def read_pic(fn):
    """
    read_pic
    :param fn:
    :return:
    """
    fnimg = cv2.imread(fn)
    img = cv2.resize(fnimg, (500, 400))
    w = img.shape[1]
    h = img.shape[0]
    w_interval = w / w_fg
    h_interval = h / h_fg

    alltz = []
    for now_h in xrange(0, h, h_interval):
        for now_w in xrange(0, w, w_interval):
            b = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 0]
            g = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 1]
            r = img[now_h:now_h + h_interval, now_w:now_w + w_interval, 2]
            btz = np.mean(b)
            gtz = np.mean(g)
            rtz = np.mean(r)
            alltz.append([btz, gtz, rtz])
    result_alltz = np.array(alltz).T
    pca = mlpy.PCA()
    pca.learn(result_alltz)
    result_alltz = pca.transform(result_alltz, k=len(result_alltz) / 2)
    result_alltz = result_alltz.reshape(len(result_alltz))
    return result_alltz


train_x = []
d = []
sp_d = []
sp_d.append([0, 0, 1])
sp_d.append([0, 1, 0])
sp_d.append([1, 0, 0])

for ii in xrange(1, 4):
    for jj in xrange(1, 3):
        fn = '/home/abc/Projects/machine_learning/img/base/p' + str(ii) + '-' + str(jj) + ".jpg"
        pictz = read_pic(fn)
        train_x.append(pictz)
        d.append(sp_d[ii - 1])

myinput = np.array(train_x)
mytarget = np.array(d)
mymax = np.max(myinput)
netminmax = []
for i in xrange(len(myinput[0])):
    netminmax.append([0, mymax])

bpnet = nl.net.newff(netminmax, [5, 3])

err = bpnet.train(myinput, mytarget, epochs=800, show=5, goal=0.2)

test_base = "/home/abc/Projects/machine_learning/img/base/test{}.jpg"

if err[-1] > 0.4:
    print err
    print 'fail'
else:
    pl.subplot(111)
    pl.plot(err)
    pl.xlabel('epoch number')
    pl.ylabel('error')
    simd = bpnet.sim(myinput)
    mysimd = get_result(simd)
    print mysimd

    testpictz = np.array([read_pic(test_base.format(1))])
    simtest = bpnet.sim(testpictz)
    mysimtest = get_result(simtest)
    print simtest
    print mysimtest

    testpictz = np.array([read_pic(test_base.format(2))])
    simtest = bpnet.sim(testpictz)
    mysimtest = get_result(simtest)
    print simtest
    print mysimtest

    testpictz = np.array([read_pic(test_base.format(3))])
    simtest = bpnet.sim(testpictz)
    mysimtest = get_result(simtest)
    print simtest
    print mysimtest

    testpictz = np.array([read_pic(test_base.format(4))])
    simtest = bpnet.sim(testpictz)
    mysimtest = get_result(simtest)
    print simtest
    print mysimtest

    pl.show()
