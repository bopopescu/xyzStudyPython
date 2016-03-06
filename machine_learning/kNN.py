#! /data/server/python/bin/python
# -*- coding:utf-8 -*-
"""
k-近邻算法
"""
import math
import operator
from collections import Counter


def knn(position, data_set, labels, k):
    """
    k-近邻算法
    :param position: 待分类点
    :param data_set: 数据样本
    :param labels: 标签集合
    :param k: 取值
    :return: 所属标签
    """
    distance_list = []
    for index, item in enumerate(data_set):
        distance_list.append((
            labels[index],
            math.sqrt(reduce(operator.add, [(v - position[i]) ** 2 for i, v in enumerate(item)]))
        ))
    distance_list = sorted(distance_list, key=lambda x: x, reverse=True)
    result = Counter([val[0] for val in distance_list[:k]])
    result_labels = sorted(result.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    return result_labels[0][0]


if __name__ == "__main__":
    point = [0.2, 0.3]
    data_set = [[1, 1.1], [1, 1], [0, 0], [0, 0.1]]
    labels = ['A', 'A', 'B', 'B']
    k = 3
    print knn(point, data_set, labels, k)
