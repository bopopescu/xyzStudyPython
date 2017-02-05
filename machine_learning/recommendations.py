#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: recommendations.py
@date: 2016-11-17
"""
__author__ = "abc"

from math import sqrt


def sim_distance(prefs, person1, person2):
    """dtype

    :param prefs:
    :param person1:
    :param person2:
    :return:
    """
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0:
        return 0

    sum_of_squares = sum(
        [pow(prefs[person1][item] - prefs[person2][item], 2) for item in prefs[person1] if item in prefs[person2]]
    )

    return 1 / (1 + sqrt(sum_of_squares))
