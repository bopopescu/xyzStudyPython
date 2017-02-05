#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
摘    要: jieba_demo.py
创 建 者: zhangxu
创建日期: 2016-11-10
"""
__auhor__ = "zhangxu"
import codecs
import pdb
import chardet
import jieba


def format_coding(strs, encoding="utf-8"):
    """format_coding"""
    if isinstance(strs, unicode):
        return strs.encode(encoding)
    detcoding = chardet.detect(strs)["encoding"]
    if detcoding == encoding:
        return strs
    return strs.decode(detcoding).encode(encoding)


def loadData():
    with open("/home/abc/Projects/jieba_demo/data/raw_export_data.txt", "r") as f:
        datas = f.readlines()
    return datas[1:]


def cutData(dl):
    new_datas = []
    for item in dl:
        title, category = item.split("\t")
        gen_item = jieba.cut(title, cut_all=False)
        item_list = list(set([format_coding(val) for val in gen_item if val.strip() and not val.isdigit()]))
        item_list.insert(0, format_coding(category.replace("\n", "").strip()))
        item_str = " ".join(item_list)
        new_datas.append(item_str)
        print item_str
    return new_datas


def saveNewData(datas):
    with open("/home/abc/Projects/jieba_demo/data/new_export_data2.txt", "wb") as f:
        f.write("\n".join(datas))


if __name__ == "__main__":
    datas = loadData()
    new_datas = cutData(datas)
    saveNewData(new_datas)
