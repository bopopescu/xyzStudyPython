#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: tb_raw.py
@date: 2017-02-05
"""
__author__ = "abc"

from peewee import (
    IntegerField, DateTimeField, CharField, PrimaryKeyField
)

from peewee import MySQLDatabase, Model


class TbRaw(Model):

    """
    """
    id = PrimaryKeyField()
    name = CharField()
    age = IntegerField()
    create_time = DateTimeField()

    class Meta(object):

        """表配置信息
        """
        database = MySQLDatabase(database="xyz", host="127.0.0.1", password="xyz2011", user="root", port=3306)
        db_table = "tb_raw"
