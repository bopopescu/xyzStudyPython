#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: main.py
@date: 2017-02-04
"""
__author__ = "abc"

from peewee import SelectQuery
from model.db.tb_raw import TbRaw

if __name__ == "__main__":
    # query = TbRaw.select().where(TbRaw.id > 0)
    query = SelectQuery(TbRaw).where(TbRaw.id > 0)
    print query.sql()[0] % tuple(query.sql()[1])
    for item in query.dicts().execute():
        print item

    # UNION查询
    query = TbRaw.select().where(TbRaw.id >= 2) | TbRaw.select().where(TbRaw.id < 2)
    print query.sql()[0] % tuple(query.sql()[1])
    for item in query.dicts().execute():
        print item
