#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: do_participle.py
@date: 2016-11-16
"""
__author__ = "abc"

import os
import sys

sys.path.insert(0, "/" + os.path.join(*os.path.split(os.path.realpath(__file__))[0].split("/")[:-1]))

from lib.mongo import MongoClient
from lib.categorys.participle import Participle


def do_participle():
    """
    do_participle
    :return:
    """
    mc = MongoClient()
    pt = Participle(mc)
    pt.load_data()
    pt.do_participle()


if __name__ == "__main__":
    do_participle()
