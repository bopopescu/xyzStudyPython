#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import pymongo

MONGODB_STR = "mongodb://127.0.0.1:27017"


class MongoClient(object):

    def __init__(self):
        """
        init
        :return:
        """
        connection = pymongo.MongoClient(MONGODB_STR)
        self.db = connection["tbk"]
