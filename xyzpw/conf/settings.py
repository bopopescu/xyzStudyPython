#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2015,掌阅科技
All rights reserved.

File Name: config.py
Author: tanshuai
Created on: 2015-06-16
'''
import yaml
import sys


class ConfError(Exception):
    """配置出错异常信息
    """
    pass


class AttrDict(dict):

    '''用于将dict通过[]来取值的方式改为.来取值
    举例：
    >>> test_dict = {'abc':123}
    >>> test_dict = AttrDict(test_dict)
    >>> test_dict.abc
    ... 123
    '''

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            return None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def __repr__(self):
        return '<Storage ' + dict.__repr__(self) + '>'

    def __getstate__(self):
        return dict(self)

    def __setstate__(self, value):
        for k, v in value.items():
            self[k] = v

CONF = """
DATABASE:
  xyz:
    master: 'mysql://root:xyz2011@127.0.0.1:3306/xyz'
    slaves:
      - 'mysql://root:xyz2011@127.0.0.1:3306/xyz'
DATABASE_MAP:
  xyz: 'XYZ_DB'
"""
DATA = yaml.load(CONF)
CONFIG = AttrDict(DATA)
sys.modules['conf.settings'] = CONFIG
