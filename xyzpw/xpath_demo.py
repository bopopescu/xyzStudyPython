#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: xpath_demo.py
@date: 2017-02-04
"""
__author__ = "abc"

import lxml.html

import requests


if __name__ == "__main__":
    url = "http://noogel.xyz"
    res = requests.get(url)
    doc = lxml.html.document_fromstring(res.content)
    title_xpath = ".//header[@id='header']//a[@class='brand']/span[@class='site-title']"
    print doc.xpath(title_xpath)[0].text
