#!/usr/bin/python
# -*- coding:utf-8 -*-
__author__ = 'xyz'
import time
from functools import wraps


def argv_to_dict(argv):
    args = {}
    for arg in argv:
        try:
            kv_list = arg.split("=")
            if kv_list[0].startswith("--"):
                kv_list[0] = kv_list[0][2:]
            elif kv_list[0].startswith("-"):
                kv_list[0] = kv_list[0][1:]
            args[kv_list[0]] = kv_list[1]
        except IndexError:
            pass
        except Exception, ex:
            print ex
    return args


def fn_timer(function):
    """
    程序执行时间
    :param function:
    :return:
    """
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" % (function.func_name, str(t1-t0)))
        return result
    return function_timer