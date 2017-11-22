#!/usr/bin/python
# coding: utf-8
"""
File: demo.py
Author: zhangxu01 <zhangxu01@zhihu.com>
Date: 2017-08-28 22:59
Description: demo
"""
import logging

import tornado

from tornado import gen, web

logging.basicConfig(
    format="[%(asctime)s %(filename)s line:%(lineno)d %(levelname)s] %(message)s"
)
logger = logging.getLogger("tornado")
logger.setLevel(logging.DEBUG)


@gen.coroutine
def service_method():
    raise gen.Return("abc")


class NoBlockHandler(tornado.web.RequestHandler):

    @web.asynchronous
    @gen.coroutine
    def get(self):
        result = yield service_method()
        self.write(result)
        self.finish()


class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            "xsrf_cookies": False,
        }
        handlers = [
            (r"/api/noblock", NoBlockHandler),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    Application().listen(2345)
    tornado.ioloop.IOLoop.instance().start()
