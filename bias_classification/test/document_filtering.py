#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import re
import chardet
import math

from lib.mongo import MongoClient


def getwords(doc):
    """分裂字符串用"""
    # splitter = re.compile('\\W*')
    # words = [val.lower() for val in splitter.split(doc) if 2 < len(val) < 20]
    words = [val.lower() for val in doc.split(" ") if 1 < len(val) < 10]
    return {key: 1 for key in words}


class Classifier(object):
    def __init__(self, getfeatures, filename=None):
        # 统计特征/分类组合的数量
        self.fc = {}
        # 统计每个分类中的文档数量
        self.cc = {}
        self.getfeatures = getfeatures

        self.thresholds = {}

    def incf(self, f, cat):
        """增加对特征/分类组合的计数值"""
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incc(self, cat):
        """增加对某一分类的计数值"""
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def fcount(self, f, cat):
        """某一特征出现于某一分类中的次数"""
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    def catcount(self, cat):
        """属于某一分类的内容项数量"""
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0

    def totalcount(self):
        """所有内容项的数量"""
        return sum(self.cc.values())

    def categories(self):
        """所有分类的列表"""
        return self.cc.keys()

    def train(self, item, cat):
        """增加训练数据"""
        features = self.getfeatures(item)
        # 针对该分类为每个特征增加计数值
        for f in features:
            self.incf(f, cat)
        # 增加针对该分类的计数值
        self.incc(cat)

    def fprob(self, f, cat):
        """计算特征在分类下的概率"""
        if self.catcount(cat) == 0: return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        """计算加权概率"""
        basicprob = prf(f, cat)
        totals = sum([self.fcount(f, c) for c in self.categories()])
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp

    def setthreshold(self, cat, t):
        """设置阀值"""
        self.thresholds[cat] = t

    def getthreshold(self, cat):
        """获取阀值"""
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]


class Naivebayes(Classifier):
    def docprob(self, item, cat):
        """计算所有特征概率相乘的整体概率"""
        features = self.getfeatures(item)
        p = 1
        for f in features: p *= self.weightedprob(f, cat, self.fprob)
        return p

    def prob(self, item, cat):
        """计算分类的概率"""
        catprob = self.catcount(cat) / self.totalcount()
        docprob = self.docprob(item, cat)
        return docprob * catprob

    def classify(self, item, default=None):
        """获取特征的在不同分类下的最大概率"""
        probs = {}
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
                max = probs[cat]
                best = cat

        for cat in probs:
            if cat == best: continue
            if probs[cat] * self.getthreshold(best) > probs[best]: return default, max

        return best, max


def sampletrain(nb, m, selected_type="accurate"):
    """

    :param nb:
    :return:
    """
    for item in m.db.bias_participle.find():
        nb.train(item[selected_type], item["category"])


def format_coding(strs, encoding="utf-8"):
    """format_coding"""
    if isinstance(strs, unicode):
        return strs.encode(encoding)
    detcoding = chardet.detect(strs)["encoding"]
    if detcoding == encoding:
        return strs
    return strs.decode(detcoding).encode(encoding)


if __name__ == "__main__":
    m = MongoClient()
    nb = Naivebayes(getwords)
    participle_type = ["whole", "accurate", "search"]
    selected_type = participle_type[2]
    # 训练
    sampletrain(nb, m, selected_type=selected_type)
    diff_count = 0
    all_count = m.db.bias_test.count()
    for item in m.db.bias_test.find():
        bias_category = nb.classify(item[selected_type], default="")[0]
        real_category = item["category"]
        title = item["title"]
        if bias_category != real_category:
            diff_count += 1
            # print format_coding(bias_category), format_coding(real_category), format_coding(title)
    print selected_type, "{:.2f}%".format(100 - float(diff_count) / float(all_count) * 100)
