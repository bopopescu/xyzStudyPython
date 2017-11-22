__author__ = 'xyz'
import sys
import socket
import urllib, urllib2
from xyz_lib import utils


class ScanNetwork(object):
    """
    plan next:
    op:
    o: one
    m: mulit
    f:
    """

    def __init__(self, op=None, ip=None, port=None, **kwargs):
        self.op = op
        self.ip = ip
        self.port = port
        self.kwargs = kwargs
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status_dict = {0: "open", 1: "error", 5: "timeout", 111: "close"}

    def tcp_ping(self):
        '''
        tcp_ping
        :return:
        '''
        if not self.ip or not self.port:
            print "ip or port is None"
        self.__try_connect()
        print "Address:%s is %s" % (self.__format_address(), self.status_dict[self.status])

    def __try_connect(self, timeout=5):
        '''
        connect to address(ip,port)
        :param timeout:
        :return:
        '''
        self.status = self.socket.connect_ex((self.ip, self.port))
        self.socket.settimeout(timeout)

    def __format_address(self):
        '''
        format address to ip:port
        :return:
        '''
        return "%s:%s" % (self.ip, self.port)


class Splider():

    def __init__(self):
        self.proxy = {}
        pass

    def set_proxy(self, proxy_url):
        self.proxy = {"http": proxy_url}

    # print ""n".join(["%s=%s" % (k, v) for k, v in os.environ.items()])
    # print os.getenv("http_proxy")
    # import os
    # os.putenv("http_proxy", "http://proxyaddr:<port>")

    @classmethod
    def get_content(self, url):
        s = urllib2
        opener = s.build_opener(s.ProxyHandler({"http", "http://127.0.0.1:8087"}))
        s.install_opener(opener)
        b = (s == urllib2)
        response = urllib2.urlopen(url, proxies=self.proxy)
        content = response.read()
        headeer = response.info()
        print content
        print headeer


if __name__ == "__main__":
    args = utils.argv_to_dict(sys.argv)
    # scannetwork
    # if "ip" in args and "port" in args:
    #     scan_network = ScanNetwork(None, str(args["ip"]), int(args["port"]))
    #     scan_network.tcp_ping()
    Splider.get_content("http://www.baidu.com")
