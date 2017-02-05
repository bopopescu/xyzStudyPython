#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import pymongo

from conf import settings

MONGODB_STR = "mongodb://127.0.0.1:27017"


class MongoClient(object):

    def __init__(self):
        """
        init
        :return:
        """
        connection = pymongo.MongoClient(MONGODB_STR)
        self.db = connection["itao"]

    @property
    def excel_data(self):
        """
        excel_data collection
        :return:
        """
        return self.db.excel_data_v2
        # return self.db.excel_data
