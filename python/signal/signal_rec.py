#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '6/2/16'
"""
__author__ = 'root'


import os
import time
import signal


def rec_signal(a, b):
    """

    :param a:
    :param b:
    :return:
    """
    import pdb
    pdb.set_trace()
    print "@@@@@@rec"
    print "a", a
    print "b", b
    print "@@@@@@rec"

signal.signal(signal.SIGTERM, rec_signal)


print "my pid is:", os.getpid()

while 1:
    time.sleep(10)
