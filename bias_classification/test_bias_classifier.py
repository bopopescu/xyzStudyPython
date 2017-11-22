#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: bias_classifier.py
@date: 2016-11-12
"""
__author__ = "abc"

import pdb

from lib.mongo import MongoClient
from lib.utils import format_coding
from bias_classifier import BiasClassifier


def test_bias_classifier():
    """
    测试贝叶斯分类器
    :return:
    """
    selected_type = "whole"
    mongo = MongoClient()
    bias = BiasClassifier()
    # 训练
    for item in mongo.db.bias_participle.find():
        bias.train(item[selected_type], item["category"])

    diff_count = 0
    all_count = mongo.db.bias_test.count()
    for item in mongo.db.bias_test.find():
        bias_category = bias.classify(item[selected_type])[0]
        real_category = item["category"]
        title = item["title"]
        if bias_category != real_category:
            diff_count += 1
            print format_coding(bias_category), format_coding(real_category), format_coding(title)
    print selected_type, "{:.2f}%".format(100 - float(diff_count) / float(all_count) * 100)


if __name__ == "__main__":
    test_bias_classifier()



