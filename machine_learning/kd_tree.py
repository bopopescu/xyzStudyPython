#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: kd_tree.py
@date: 2016-12-28
@desc: kd树
"""
__author__ = "abc"
import math
import matplotlib as mp


class KDNode(object):
    """
    kd-node
    """

    def __init__(self, value):
        """
        __init__
        :param value:
        """
        self.value = value
        self.__left = None
        self.__right = None
        self.__parent = None

    @property
    def left(self):
        """
        left
        :return:
        """
        return self.__left

    @property
    def right(self):
        """
        right
        :return:
        """
        return self.__right

    @property
    def parent(self):
        """
        parent
        :return:
        """
        return self.__parent

    def set_left(self, node):
        """
        set_left
        :param node:
        :return:
        """
        if not node:
            return
        self.__left = node
        node.parent = self

    def set_right(self, node):
        """
        set_right
        :param node:
        :return:
        """
        if not node:
            return
        self.__right = node
        node.parent = self

    def __str__(self):
        """
        __str__
        :return:
        """
        return str(self.value)

    def is_leaf(self):
        """
        is_leaf
        :return:
        """
        return not self.__left and not self.__right

    def is_root(self):
        """
        is_root
        :return:
        """
        return not self.__parent


def create_data():
    """
    create_data
    :return:
    """
    return [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]


def build_kd_tree(data, deep=0):
    """
    构造kd树
    :param data:sudo apt-get install python-sklearn
    :return:
    """
    if not data:
        return
    sort_data = sorted(data, key=lambda node: node[deep % len(data[0])])
    mid_index = (len(sort_data) / 2) if len(sort_data) % 2 else (len(sort_data) / 2)
    root_node = sort_data[mid_index]
    left_data = sort_data[:mid_index]
    right_data = sort_data[mid_index + 1:]
    root = KDNode(root_node)
    root.set_left(build_kd_tree(left_data, deep + 1))
    root.set_right(build_kd_tree(right_data, deep + 1))
    return root


def search_kd_tree(tree, node, now_min_path=-1, deep=0):
    """
    search_kd_tree
    :param tree:
    :param node:
    :param deep:
    :return:
    """
    wei = deep % len(tree.value)
    value = tree.value
    min_path = (sum([(value[index] - node[index]) ** 2 for index in xrange(len(value))])) ** 0.5
    if now_min_path == -1 or now_min_path < min_path:
        now_min_path = min_path
    if node[wei] < value[wei]:
        return search_kd_tree(value.left, node, now_min_path=now_min_path, deep=deep + 1)
    else:
        return search_kd_tree(value.right, node, now_min_path=now_min_path, deep=deep + 1)


def draw_kd_tree(tree):
    """
    draw_kd_tree
    :param tree:
    :return:
    """
    pass


if __name__ == "__main__":
    data = create_data()
    kd_tree = build_kd_tree(data)
    import pdb

    pdb.set_trace()
