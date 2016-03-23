#!/usr/bin/python
# -*-coding:UTF-8 -*-

# author: 初行
# qq: 121866673
# mail: zxbd1016@163.com
# time: 2014/10/5

import urllib
import urllib2
import cookielib

# cookie set
# 用来保持会话
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# default header
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Referer': 'http://202.206.1.163/logout.do'
}

def geturlopen(hosturl, postdata={}, headers=HEADER):
    """
    operate method
    :param hosturl:
    :param postdata:
    :param headers:
    :return:
    """
    # encode postdata
    enpostdata = urllib.urlencode(postdata)
    # request url
    urlrequest = urllib2.Request(hosturl, enpostdata, headers)
    # open url
    urlresponse = urllib2.urlopen(urlrequest)
    # return url
    return urlresponse