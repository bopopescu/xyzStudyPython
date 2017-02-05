#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'

import json
import logging
import random

import requests


class ProxyPoll(object):
    """

    """
    def __init__(self):
        self.poll = []
        self._pull_poll()

    def _pull_poll(self):
        try:
            logging.info("@@@ get proxy.")
            resp = requests.get("http://127.0.0.1:7500/?per_page=10000&http_anonymous=2").json()
            if resp["code"] == 0:
                self.poll = resp["list"]
        except Exception as ex:
            logging.error(ex, exc_info=True)

    def __call__(self, *args, **kwargs):
        while not len(self.poll):
            logging.warning("@@@ not proxy, reget.")
            self._pull_poll()
        proxy_item = self.poll.pop(random.randint(0, len(self.poll) - 1))
        proxy = "http://{}:{}".format(proxy_item["ip"], proxy_item["port"])
        logging.info("@@@ get proxy:%s", proxy)
        return proxy