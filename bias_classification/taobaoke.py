#! /data/sever/python/bin/python
# -*- coding:utf-8 -*-
"""
@author: 'root'
@date: '9/30/16'
"""
__author__ = 'root'
import time
import datetime

from lib.utils import format_list
from lib.mongo import MongoClient
from lib.crawler import Crawler


class Taobaoke(MongoClient):
    """
    Taobaoke
    """
    start_urls = (
        'http://pub.alimama.com/promo/item/channel/index.htm?channel=qqhd&toPage={}&catIds={}&level=1&perPageSize=100'
    )
    crawler = Crawler()

    def start_requests(self):
        # item list range
        for cat in range(1, 18):
            for page in range(10, 31):
                print "crawl:%s,%s" % (cat, page)
                self.requests_url(self.start_urls.format(page, cat), callback=self.callback)

    def requests_url(self, url, callback=None):
        """

        :param url:
        :param callback:
        :return:
        """
        crawler = self.crawler.crawl(url)
        callback(crawler)

    def safe_febx_text(self, crawler, xpath, count=1, max_count=10):
        """

        :param crawler:
        :param xpath:
        :param count:
        :param max_count:
        :return:
        """
        if count > max_count:
            return ""
        try:
            return crawler.febx(xpath).text.strip()
        except Exception:
            print "try:%s" % count
            return self.safe_febx_text(crawler, xpath, count=count+1, max_count=max_count)

    def callback(self, crawler):
        """
        回调处理
        :param crawler:
        :return:
        """
        time.sleep(10)
        for index in range(1, 101):
            item = {
                "title": self.safe_febx_text(
                    crawler,
                    u".//*[@id='J_search_results']/div/div[{}]"
                    u"/div[@class='box-content']/div[1]/p/a/node()".format(index)
                ),
                "category": self.safe_febx_text(
                    crawler,
                    u".//*[@class='top-nav-tag']/span"
                )
            }
            if not item["title"] or not item["category"] or self.db.tbk_test.find({"title": item["title"]}).count():
                print "continue", item["category"], item["title"]
                continue

            print item["category"], item["title"]
            self.db.tbk_test.insert(item)


if __name__ == "__main__":
    tbk = Taobaoke()
    tbk.start_requests()
