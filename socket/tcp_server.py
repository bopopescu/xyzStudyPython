#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '3/2/16'
"""
__author__ = 'root'

import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

print "Listen:%s" % ((bind_ip, bind_port),)


def handle_client(client_socket):
    request = client_socket.recv(1024)
    print "Recv:%s" % request
    client_socket.send("ACK!")
    client_socket.close()

while True:
    client, addr = server.accept()
    print client, addr
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
