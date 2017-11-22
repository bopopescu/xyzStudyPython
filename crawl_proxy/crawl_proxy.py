#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@creator xyz
@time:2015-8-23
@desc:爬虫代理
@version: v3.0 单独脚本
"""
__version__ = "v3.0"
import os
import re
import sys
import json
import datetime
import requests
import signal
import gevent
from gevent import monkey
from gevent.queue import Queue
from lxml import etree
# gevent.signal(signal.SIGQUIT, gevent.shutdown)

from splinter import Browser

monkey.patch_socket()

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"}
HTTP_TEST_URL = 'httpbin.org/get'
MY_IP = "123.66.243.46"


def test_https_ip(**kwargs):
    """验证是否支持https
    """
    try:
        r = requests.get("https://" + HTTP_TEST_URL, **kwargs)
        if r.status_code == 200:
            return 1
    except Exception as ex:
        print("https:%s", ex)
    return 0


def test_proxy(proxy=None, test_https=False):
    """
    测试代理是否可用
    """
    kwargs = {"headers": UA, "timeout": 30}
    if proxy:
        kwargs["proxies"] = {"http": "http://" + proxy}
    is_https = 0
    response = requests.get("http://" + HTTP_TEST_URL, **kwargs)
    if response.status_code != 200:
        raise Exception("Status code: {0}".format(response.status_code))
    delay = response.elapsed.microseconds
    is_anonymous = 0 if json.loads(response.text)["origin"].find(MY_IP) >= 0 else 1
    if test_https:
        is_https = test_https_ip(**kwargs)
    return proxy, delay, is_anonymous, is_https


def get_url_text(url):
    """
    从网页中获取
    """
    try:
        kwargs = {"headers": UA}
        r = requests.get(url, **kwargs)
        if r.status_code != 200:
            return ""
        return r.text
    except Exception as ex:
        return ""


def fetch_dynamic(url, timeout=30):
    """
    获取动态页面内容
    """
    browser = Browser('phantomjs', user_agent=UA, load_images=False,
                      wait_time=timeout)
    browser.visit(url)
    body = browser.html
    browser.quit()
    return body


def extract(reg, body, multi=True):
    """
    从网页正文中提取内容

    @reg 表达式
    @body 网页正文
    @multi 获取多个内容
    """
    if reg.startswith("reg:"):
        results = re.findall(reg[4:], body)
    else:
        if isinstance(body, unicode):
            body = etree.HTML(body)
        if not isinstance(body, str):
            results = body.xpath(reg)
        else:
            return []
    if multi:
        return results
    else:
        return None if len(results) == 0 else results[0]


def save_file(w_str):
    """
    write file
    :param w_str:
    :return:
    """
    file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S.csv")
    with open(file_name, "w") as f:
        f.write(w_str)
    print "Saved to file: {0}".format(file_name)


class Proxy(object):
    """
    item
    """

    def __init__(self):
        self.tasks = Queue()
        self.wait_test_list = []
        self.span_count = 10
        self.proxy_set = set()
        self.gevent_timeout = 10

    @classmethod
    def inst(cls):
        """
        单例
        """
        name = 'instance'
        if not hasattr(cls, name):
            setattr(cls, name, cls())
        return getattr(cls, name)

    def add_to_queue(self):
        for proxy in self.wait_test_list:
            if proxy:
                self.tasks.put_nowait(proxy)

    def add(self):
        """
        验证老代理 & 添加新代理
        """
        result = []

        # 测试好用的
        result.extend(KuaiProxy().proxy_list())
        for i in xrange(1, 3):
            result.extend(CommonProxy(0).proxy_list(
                "http://www.xicidaili.com/nn/%s" % i,
                ".//table[@id='ip_list']/tr[position()>1]",
                "td[3]/text()", "td[4]/text()"))

        self.wait_test_list = list(set(result))
        print "Wait test proxy: {0}.{1}.".format(
            ",".join(self.wait_test_list), len(self.wait_test_list)
        )
        # 添加到待测试队列
        gevent.spawn(self.add_to_queue).join()
        try:
            # 启动span_count个测试协程
            gevent.joinall([gevent.spawn(self.test_ip) for _ in range(self.span_count)])
        except Exception as ex:
            print ex
        proxy_list = list(self.proxy_set)
        proxy_list.insert(0, "代理IP,延迟时间,是否匿名,HTTP,HTTPS")
        if self.proxy_set:
            print "Save proxy: {0}.{1}.".format(",".join(proxy_list), len(proxy_list))
            save_file("\n".join(proxy_list))

    def test_ip(self):
        """
        测试并添加IP
        """
        while not self.tasks.empty():
            item = self.tasks.get()
            try:
                if not item:
                    continue
                proxy_ip = None
                with gevent.Timeout(self.gevent_timeout, False):
                    proxy_ip, delay, is_anonymous, is_https = test_proxy(item)
                if not proxy_ip:
                    print "Proxy timeout: {0}".format(item)
                    continue
                self.proxy_set.add("{proxy},{delay},{anonymous},{http},{https}".format(
                    proxy=item,
                    delay=delay,
                    anonymous=is_anonymous,
                    http=1, https=-1
                ))
                print "Success saved proxy: {0}".format(item)
            except Exception as ex:
                print "Test proxy error: {0} {1}".format(item, ex)
        print "Queue is empty, exist."


class ProxyItemBase(object):
    """
    item
    """

    def __init__(self, is_dynamic_page=0):
        self.is_dynamic_page = is_dynamic_page

    def proxy_list(self):
        """
        proxy list
        """
        pass

    def get_proxy_list(self, url, tr_reg, ip_reg, port_reg=None):
        """
        join类型proxy
        """

        try:
            print "Start fetch URL: {0}".format(url)
            if not self.is_dynamic_page:
                text = get_url_text(url)
            else:
                text = fetch_dynamic(url)
            proxy_list = []

            for tr in self.get_tr_data(text, tr_reg):
                result = self.get_td_proxy(tr, ip_reg, port_reg)
                if isinstance(result, list):
                    proxy_list.extend(result)
                else:
                    proxy_list.append(result)
            return proxy_list

        except Exception as ex:
            return []

    def get_tr_data(self, body, tr_reg):
        """
        获取行数据
        """
        return extract(tr_reg, body)

    def get_td_proxy(self, tr, ip_reg, port_reg=None):
        """
        获取ip:port
        """

        if port_reg:
            proxy_ip = "%s:%s" % (extract(ip_reg, tr, False).strip(),
                                  extract(port_reg, tr, False))
        else:
            proxy_ip = extract(ip_reg, tr, False)

        return proxy_ip.strip().replace("http://", "")


class CommonProxy(ProxyItemBase):
    """
    通用
    """

    def __init__(self, is_dynamic_page=0):
        super(CommonProxy, self).__init__(is_dynamic_page)

    def proxy_list(self, url, tr_reg, ip_reg, port_reg=None):
        """
        proxy list
        """
        return self.get_proxy_list(url, tr_reg, ip_reg, port_reg)


class KuaiProxy(ProxyItemBase):
    """快速代理"""

    def proxy_list(self):
        """
        proxy list
        """
        result = []
        url = "http://www.kuaidaili.com/free/inha/%s/"
        for i in xrange(1, 10):
            real_url = url % i
            tr_reg = "//div[@id='list']/table/tbody/" \
                     "tr|//div[@id='list']/table/tr"
            ip_reg = "td[1]/text()"
            port_reg = "td[2]/text()"
            p_list = self.get_proxy_list(real_url, tr_reg, ip_reg, port_reg)
            result.extend(p_list)

        return result


class TxtProxy(ProxyItemBase):
    """
    全文本类型基础类
    """

    def proxy_list(self, url, tr_reg):
        """
        proxy list
        """
        try:
            return self.get_proxy_list(url, tr_reg, None)
        except Exception as ex:
            return []

    def get_tr_data(self, body, tr_reg):
        """
        获取行数据
        """
        return body.split(tr_reg)

    def get_td_proxy(self, tr, ip_reg, port_reg=None):
        """
        获取ip:port
        """
        return tr.replace("http://", "")


if __name__ == "__main__":
    Proxy.inst().add()
