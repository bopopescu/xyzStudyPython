#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '3/6/16'
"""
__author__ = 'root'
# import logging
# logging = logging.getLogger()
# logging.setLevel(logging.DEBUG)
# # 创建一个handler，用于写入日志文件
# fh = logging.FileHandler('test.log')
# fh.setLevel(logging.DEBUG)
# # 再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# # 定义handler的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# # 记录一条日志
# logger.info('foorbar')
import logging
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(filename)s Line:%(lineno)d] %(message)s',
    datefmt='%m%d%H%M%S',
    # filename='test.log',
    # filemode='w',
    level=logging.INFO
)
logging.debug('This message should appear on the console')
logging.info('This message should appear on the console')