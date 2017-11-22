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

M = MongoClient().db.tbk_test.find()

M = [val for val in M]

e = Excel()

title = [
('title', '名称'),
('category', '分类'),
]
with open('export_date.xls', 'wb') as f:
    f.write(e.generate(title, M))

