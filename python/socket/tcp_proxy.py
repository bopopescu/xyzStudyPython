#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '3/6/16'
"""
__author__ = 'root'


import sys
import socket
import logging
import threading
from optparse import OptionParser




class TcpProxy(object):
    """

    """
    def __init__(self):
        self.port = 1987
        self.max_client = 10
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def server_loop(self):
        """

        :return:
        """
        try:
            # 绑定监听
            self.server.bind(("0.0.0.0", self.port))
            self.server.listen(self.max_client)
        except Exception as ex:
            logging.debug(ex, exc_info=True)
