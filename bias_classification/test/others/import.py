#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'
import time
import datetime

from lib.utils import format_list
from lib.mongo import MongoClient
from lib.crawler import Crawler
from lib.excel import Excel

M = MongoClient()


def f():
    with open('/home/abc/Projects/bias_classification/data/new_export_data2.txt', 'r') as f:
        datas = f.readlines()

    print M.db.tbk_disp.remove()
    for item in datas:
        cate, title = item.split(' ', 1)
        title = title.replace("\n", "")
        if M.db.tbk_disp.find({"title": title}).count():
            print "continue", title
            continue
        M.db.tbk_disp.insert({"category": cate, "title": title})


if __name__ == "__main__":
    f()

