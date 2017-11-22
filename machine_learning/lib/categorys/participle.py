#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: participle.py
@date: 2016-11-12
"""
__author__ = "abc"

import random

import jieba

from lib.utils import format_coding


def filter_word(gen_item):
    """
    过滤分词结果
    :param gen_item:
    :return:
    """
    return " ".join(list(set([format_coding(val) for val in gen_item if val.strip() and not val.isdigit()])))


class Participle(object):
    """

    """

    def __init__(self, mc):
        """
        __init__
        """
        self.mongo = mc.db
        self.category = self.mongo.bias_category
        self.participle = self.mongo.bias_participle
        self.test = self.mongo.bias_test
        self.data = []

    def load_data(self):
        """
        加载数据
        :return:
        """
        with open('/home/abc/Projects/autotbk/lib/categorys/data/raw_export_data.txt', 'r') as f:
            datas = f.readlines()

        for item in datas:
            title, category = item.split("\t")
            category = category.replace("\n", "")
            if self.category.find({"title": title}).count():
                print "continue", title
                continue
            self.category.insert({"category": category, "title": title})

    def do_participle(self):
        """
        分词
        :return:
        """
        for item in self.category.find():
            whole = filter_word(jieba.cut(item["title"], cut_all=True))
            accurate = filter_word(jieba.cut(item["title"], cut_all=False))
            search = filter_word(jieba.cut_for_search(item["title"]))
            # pdb.set_trace()
            participle_item = {
                "whole": whole,
                "accurate": accurate,
                "search": search,
                "title": item["title"],
                "category": item["category"]
            }
            find_exists_item = {
                "title": item["title"]
            }
            if random.randint(1, 6) == 6:
                if self.test.find(find_exists_item).count():
                    print participle_item["title"]
                    continue
                self.test.insert(participle_item)
            else:
                if self.participle.find(find_exists_item).count():
                    print participle_item["title"]
                    continue
                self.participle.insert(participle_item)


if __name__ == "__main__":
    par = Participle("")
    par.load_data()
    par.do_participle()
