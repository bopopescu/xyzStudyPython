#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
import errno
import functools
from tornado import ioloop
import socket


def connection_ready(sock, fd, events):

    while True:
        try:
            connection, address = sock.accept()
        except socket.error, e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        print (connection, "\n####\n", address, "\n####\n", fd, "\n####\n", events)
        do_method(connection, address)


def do_method(con, add):
    while True:
        data = con.recv(1024)
        if data:
            print data

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setblocking(0)
sock.bind(("", 1123))
sock.listen(128)

# 创建一个ioloop 实例
io_loop = ioloop.IOLoop.instance()
# connection_ready 的第一个参数为 sock,即 socket 的返回值
callback = functools.partial(connection_ready, sock)
# 注册函数，第一个参数是将 sock 转换为标准的描述符，第二个为回调函数，第三个是事件类型
io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
io_loop.start()
