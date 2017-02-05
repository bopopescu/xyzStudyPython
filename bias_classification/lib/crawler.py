#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '10/12/16'
"""
__author__ = 'root'

import time
from selenium import webdriver


class Crawler(object):
    """
    Crawler
    """

    def __init__(self):
        self.driver = webdriver.Firefox()

    def crawl(self, url):
        """
        crawl
        :param url:
        :return:
        """
        self.driver.get(url)
        return self

    def febx(self, xpath):
        """
        febx
        :param xpath:
        :return:
        """
        return self.driver.find_element_by_xpath(xpath)

    def quit(self):
        self.driver.quit()
