# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import datetime
import logging
import subprocess
import MySQLdb.cursors
from twisted.enterprise import adbapi

from fang_price.lib import utils


class FangPricePipeline(object):
    """

    """
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
            'MySQLdb', db='scrapy_test',
            user='root', passwd='', cursorclass=MySQLdb.cursors.DictCursor,
            charset='utf8', use_unicode=True
        )

    def process_item(self, item, spider):
        """

        :param item:
        :param spider:
        :return:
        """
        # import pdb
        # pdb.set_trace()
        if "page_url" in item and "detail_url" in item:
            if item.db.fang_info.find({"page_url": item["page_url"]}).count():
                item.db.fang_info.update(
                    {"page_url": item["page_url"]}, {"$set": utils.remove_none_item(item)}
                )
            else:
                item.db.fang_info.insert(utils.remove_none_item(item))
        if "page_url" not in item and "detail_url" in item:
            page = item.db.fang_info.find_one({"detail_url": item["detail_url"]})
            if page:
                # 保存历史价格
                price_info = item.pop("price_info")
                if len(price_info) % 5 == 0:
                    # import pdb
                    # pdb.set_trace()
                    # 删除旧的历史价格
                    temp_count = item.db.fang_price.remove({"info_id": str(page["_id"])})
                    # 保存新的历史价格
                    for index in range(0, len(price_info), 5):
                        item.db.fang_price.insert({
                            "info_id": str(page["_id"]),
                            "record_date": price_info[index],
                            "max_price": price_info[index + 1],
                            "avg_price": price_info[index + 2],
                            "min_price": price_info[index + 3],
                            "desc": price_info[index + 4],
                            "create_time": datetime.datetime.now()
                        })
                # 更新信息
                item.db.fang_info.update(
                    {"detail_url": item["detail_url"]}, {"$set": utils.remove_none_item(item)}
                )

        return item
