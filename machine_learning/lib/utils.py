#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import os
from decimal import Decimal

import chardet
from tornado.template import Template

from conf.settings import TYPE_MAP


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


def generate_template(file_name, data_list, save_dir="data"):
    """

    :param file_name:
    :param data_list:
    :return:
    """
    file_url = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../tpl", "template.tpl")
    with open(file_url) as f:
        tpl = f.read()
    data = Template(tpl).generate(file_name=file_name, data=data_list)
    with open("{}/{}.html".format(save_dir, file_name), "wb") as f:
        f.write(data)


def format_process(index, count):
    """
    格式化进程
    :param index:
    :param count:
    :return:
    """
    rate = Decimal(str(index)) / Decimal(str(count)) * 100
    return "{:.2f}%".format(rate)


def get_category(title):
    """
    获取商品分类
    :param title:
    :return:
    """
    def find_mkey(*args):
        flag = 0
        for arg in args:
            flag = title[flag:].find(arg)
            if flag == -1:
                return False
        return True

    r = {}
    for cate, key_list in TYPE_MAP.items():
        key_count = 0
        for item in key_list:
            if isinstance(item, list):
                if find_mkey(title, *item):
                    key_count += 1
            else:
                if item in title:
                    key_count += 1
        r[cate] = key_count
    max_count = max(r.values())
    if max_count == 0:
        return "其它"
    max_c = [k for k, v in r.items() if v == max_count][0]
    return max_c


def format_coding(strs, encoding="utf-8"):
    """format_coding"""
    if isinstance(strs, unicode):
        return strs.encode(encoding)
    detcoding = chardet.detect(strs)["encoding"]
    if detcoding == encoding:
        return strs
    return strs.decode(detcoding).encode(encoding)


if __name__ == "__main__":
    from mongo import MongoClient
    date = "2016-10-16"
    mc = MongoClient()
    data = mc.db.quality_goods.find(
        {"import_date": date, "taokl": {"$ne": None}})
    generate_template(date, data)