#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: fisher_classifier.py
@date: 2016-11-14
"""
__author__ = "abc"

import math

from bias_classifier import BiasClassifier


def invchi2(chi, df):
    """
    todo 此函数需了解
    :param chi:
    :param df:
    :return:
    """
    m = chi / 2.0
    exp_sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m/i
        exp_sum += term
    return min(exp_sum, 1.0)


class FisherClassifier(BiasClassifier):
    """

    """

    def category_feature_probability(self, feature, category):
        """
        计算分类在特征下的概率
        :param feature:
        :param category:
        :return:
        """
        feature_probability = self.feature_probability(feature, category)
        all_category_feature_probability = float(sum(
            [self.feature_probability(feature, v_category) for v_category in self.category_count.keys()]))
        return feature_probability / all_category_feature_probability

    def weight_category_feature_probability(self, feature, category, seq=0.1):
        """
        加权计算分类在特征下的概率
        :param feature:
        :param category:
        :param seq:
        :return:
        """
        feature_probability = self.feature_probability(feature, category)
        all_category_feature_probability = float(sum(
            [self.feature_probability(feature, v_category) for v_category in self.category_count.keys()]))
        return (feature_probability + seq) / (all_category_feature_probability + len(self.category_count.keys()) * seq)

    def fisher_probability(self, sample, category):
        """
        费舍尔方法计算概率
        :param sample:
        :param category:
        :return:
        """
        # 计算分类在各特征下的乘积
        probability = 1.0
        features = self.splitter(sample)
        for feature in features:
            probability *= self.weight_category_feature_probability(feature, category)

        # 取自然对数，并乘-2
        fisher_score = -2 * math.log(probability)

        # 利用倒置对数卡方函数求得概率
        return invchi2(fisher_score, len(features) * 2)

    def classify(self, sample, default="unknown"):
        """
        计算分类
        :param sample:
        :param default:
        :return:
        """
        best_score, best_category = 0.0, default
        for category in self.category_count.keys():
            probability = self.fisher_probability(sample, category)
            if probability > best_score:
                best_score = probability
                best_category = category
        return best_category, best_score
