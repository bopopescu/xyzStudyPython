#!/usr/bin/python
# coding: utf-8
"""
File: demo.py
Author: zhangxu01 <zhangxu01@zhihu.com>
Date: 2017-08-28 22:59
Description: demo
"""
import random
import time
import urllib

import requests
import tornado

from tornado import gen, web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


@gen.coroutine
def async_fetch(url, method="GET", data=None, timeout=2 * 30,):
    request = url
    if isinstance(url, HTTPRequest):
        url = request.url
    if not isinstance(url, HTTPRequest):
        kwargs = {
            "connect_timeout": timeout,
            "request_timeout": timeout,
        }
        if data:
            if method == "GET":
                url += '?' + urllib.urlencode(data)
            else:
                kwargs["body"] = urllib.urlencode(data)
        request = HTTPRequest(url, method, **kwargs)

    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(request)
    raise gen.Return(response)


@gen.coroutine
def service_method():
    url = "http://127.0.0.1:2345/api/time"
    data = {
        "time": str(time.time())
    }
    response = yield async_fetch(url, data=data)
    raise gen.Return(response)


class NoBlockHandler(tornado.web.RequestHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self):
        result = yield service_method()
        self.write(result.body)
        self.finish()


class BlockHandler(tornado.web.RequestHandler):

    def get(self):
        begin_time = time.time()
        response = requests.get("http://127.0.0.1:2345/api/time", data={"time": str(begin_time)})
        self.write(response.content)
        self.finish()


class TimeHandler(tornado.web.RequestHandler):

    def get(self):
        req_time = self.get_argument("time", "")
        sleep_time = random.randint(10, 500) * 0.001
        time.sleep(sleep_time)
        self.write("b:{},s:{} => e:{}".format(req_time, sleep_time, time.time()))
        self.finish()


class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            "xsrf_cookies": False,
        }
        handlers = [
            (r"/api/noblock", NoBlockHandler),  # 非阻塞 IO 请求
            (r"/api/block", BlockHandler),  # 阻塞 IO 请求
            (r"/api/time", TimeHandler),  # 被请求接口
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """ main"""
    tornado.httpserver.HTTPServer(Application()).listen(2345)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
