#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: bias_classifier.py
@date: 2016-11-12
"""
__author__ = "abc"


class BiasClassifier(object):
    """
    贝叶斯分类器
    """

    def __init__(self, splitter=None):
        """
        __init__
        """
        # 特征映射到分类的统计计数
        self.feature_count = {}
        # 统计分类总数
        self.category_count = {}
        # 字符串分割器
        self.splitter = splitter if splitter else self._splitter

    def _splitter(self, words):
        """
        默认样本分割器
        :param words:
        :return:
        """
        return [val for val in words.split(" ") if 0 < len(val) < 5]

    def increase_category(self, category):
        """
        增加分类计数
        :param category:
        :return:
        """
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def increase_feature(self, feature, category):
        """
        增加特征到分类的统计计数
        :param feature:
        :param category:
        :return:
        """
        self.feature_count.setdefault(feature, {})
        self.feature_count[feature].setdefault(category, 0)
        self.feature_count[feature][category] += 1

    def train(self, sample, category):
        """
        训练样本
        :param sample:
        :param category:
        :return:
        """
        # 增加分类计数
        self.increase_category(category)
        for item in self.splitter(sample):
            # 增加特征统计
            self.increase_feature(item, category)

    def feature_probability(self, feature, category):
        """
        计算特征在分类下的概率
        特征 X = {x1, x2 ... xi}
        分类 Y = {y1, y2 ... yj}
        P(xi|yj)
        :param feature:
        :param category:
        :return:
        """
        feature_category_count = float(self.feature_count.get(feature, {}).get(category, 0))
        category_count = float(self.category_count.get(category, 0))
        return feature_category_count / category_count

    def multi_feature_probability(self, sample, category):
        """
        计算多个特征概率的乘积
        P(x1|yj)P(x2|yj)...P(xi|yj)
        :param sample:
        :param category:
        :return:
        """
        product_result = 1.0
        for feature in self.splitter(sample):
            # product_result *= self.feature_probability(feature, category)
            product_result *= self.laplace_correct_feature_probability(feature, category)
        return product_result

    def category_probability(self, category):
        """
        计算分类的概率
        :param category:
        :return:
        """
        category_count = float(self.category_count.get(category, 0))
        all_count = float(sum(self.category_count.values()))
        return category_count / all_count

    def sample_category_probability(self, sample, category):
        """
        计算分类在特征下的概率
        P(yj|x) = P(yj)P(x1|yj)P(x2|yj)...P(xi|yj)
        :param sample:
        :param category:
        :return:
        """
        return self.multi_feature_probability(sample, category) * self.category_probability(category)

    def classify(self, sample, default="unknown"):
        """
        计算所属分类
        :param sample:
        :return:
        """
        best_score, best_category = 0.0, default
        for category in self.category_count.keys():
            probability = self.sample_category_probability(sample, category)
            if probability > best_score:
                best_score = probability
                best_category = category
        return best_category, best_score

    def laplace_correct_feature_probability(self, feature, category, ap=0.1):
        """
        拉普拉斯校准 计算特征在分类下的概率
        特征 X = {x1, x2 ... xi}
        分类 Y = {y1, y2 ... yj}
        P(xi|yj)
        :param feature:
        :param category:
        :return:
        """
        feature_category_count = self.feature_count.get(feature, {}).get(category, 0)
        category_count = self.category_count.get(category, 0)
        return float(feature_category_count + ap) / float(category_count + ap * len(self.category_count.keys()))
