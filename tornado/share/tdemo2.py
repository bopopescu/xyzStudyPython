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

import tornado

from tornado import web


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
            (r"/api/time", TimeHandler),  # 被请求接口
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    """ main"""
    Application().listen(2346)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
