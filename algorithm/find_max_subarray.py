#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
分治策略
寻找最大字数组问题

1.最简单直接的是暴利遍历数组可求得最大子数组，时间复杂度为O(n^2)
2.采用分治策略将数组分为两个子数组去求解右如下三种情况：
    1.最大子数组在左子数组中。
    2.最大子数组在右子数组中。
    3.最大子数组跨越两个子数组中。

重点在于求最大子数组跨越两个子数组的情况。
从数组的中间点为一定点向左和向右遍历分别求得最大子数组。
然后相加得跨越两个子数组的最大子数组。

然后采用递归的方法将左子数组和右子数组继续拆分，最后当左右子数组为一个元素时结束返回。

在递归的每一层中计算完三种情况后选取当下的最大子数组情况返回。

最后得到的结果便是连续最大子数组。

采用分治策略的时间复杂度为O(nlogn)

"""
__author__ = 'xyz'

import random


def find_max_crossing_subarray(A, low, mid, high):
    """
    求跨越两个数组的最大字数组
    :param A:
    :param low:
    :param mid:
    :param high:
    :return:
    """
    left_sum = A[mid]
    left_index = mid
    sum = 0
    for left in range(mid, low - 1, -1):
        sum = sum + A[left]
        if sum > left_sum:
            left_sum = sum
            left_index = left

    right_sum = A[mid + 1]
    right_index = mid + 1
    sum = 0
    for right in range(mid + 1, high + 1):
        sum = sum + A[right]
        if sum > right_sum:
            right_sum = sum
            right_index = right
    return left_index, right_index, left_sum + right_sum


def find_max_subarray(A, low, high):
    """
    寻找数组中的最大子数组
    :param A:
    :param low:
    :param high:
    :return:
    """
    if low == high:
        return low, high, A[low]
    else:
        # 求中值
        mid = (low + high) / 2
        # 求左子数组最大子数组
        left_low, left_high, left_sum = find_max_subarray(A, low, mid)
        # 求右子数组最大子数组
        right_low, right_high, right_sum = find_max_subarray(A, mid + 1, high)
        # 求跨两个子数组的最大子数组
        cross_low, cross_high, cross_sum = find_max_crossing_subarray(A, low, mid, high)
        # 选出最大子数组
        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        elif cross_sum >= left_sum and cross_sum >= right_sum:
            return cross_low, cross_high, cross_sum


if __name__ == "__main__":
    random_list = [random.randint(-100, 100) for _ in range(100)]

    print random_list

    print find_max_subarray(random_list, 0, len(random_list) - 1)


