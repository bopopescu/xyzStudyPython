#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import chardet


def format_list(items, seporate="", replaces=None):
    """

    :param items:
    :param seporate:
    :param replaces:
    :return:
    """
    if not replaces:
        replaces = []
    replaces.extend([" ", "\r", "\n", "\t"])
    list_str = seporate.join(items)
    if replaces and isinstance(replaces, list):
        for strs in replaces:
            list_str = list_str.replace(strs, "")
    return list_str.strip()


def format_extract(hxs, xpath, seporate="", replaces=None):
    """

    :param hxs:
    :param xpath:
    :param seporate:
    :param replaces:
    :return:
    """
    return format_list(
        hxs.select(xpath).extract(),
        seporate=seporate,
        replaces=replaces)


def format_coding(strs, encoding="utf-8"):
    """format_coding"""
    if isinstance(strs, unicode):
        return strs.encode(encoding)
    detcoding = chardet.detect(strs)["encoding"]
    if detcoding == encoding:
        return strs
    return strs.decode(detcoding).encode(encoding)
