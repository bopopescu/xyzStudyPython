#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: tb1.py
@date: 2017-02-04
"""
__author__ = "abc"

from peewee import (
    IntegerField, DateTimeField, CharField, PrimaryKeyField
)

from model.db.base import XYZ_DB


class Tb1(XYZ_DB.Model):

    """
    """
    id = PrimaryKeyField()
    name = CharField()
    age = IntegerField()
    create_time = DateTimeField()

    class Meta(object):

        """表配置信息
        """
        db_table = "tb1"
