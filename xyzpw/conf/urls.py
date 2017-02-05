#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=relative-import

'''
Copyright (c) 2015,掌阅科技
All rights reserved.

摘    要: URL配置
创 建 者: tanshuai
创建日期: 2015-07-29
'''

# 这个文件只配置接口的部分,主机:端口部分配置在/conf/{env}/hosts.yaml
# from settings import HOSTS 在settings中加载指定环境的host
# 然后在这个文件中动态拼接完整的URL地址：host:port + api

import sys

from settings import HOSTS
from lib.utils import ObjectDict

DATA = {
    "drive_origin": (
        "/apollo/service?method=callStreamGetService"
        "&service.name=copyright.book.ucd&startDate=%s"
    ),
    "drive_outside_origin": (
        "/apollo/service?method=callStreamGetService"
        "&service.name=oversea.copyright.book.ucd&startDate=%s"
    )
}

COPYRIGHT = {
    "settlement_book_info": "/api/getSettlementBookInfo",
    "contract_info": "/api/getContractInfo",
    "dict_info": "/api/getDictInfo?key=%s",
    "free_comic_magazine_book_ids": "/api/getFreeComicMagazineBookIds",
    "sett_type": "/api/getContractBySettType",
    "book_price_info": "/api/getBookPriceInfo",
    "sett_currency": "/api/settCurrency",
}

ABROAD_OP = {
    "get_book_price_new": "/api/getBookPriceNew?book_id={}&scheme_id=66",
}


URLS = {}
# 获取当前文件定义的键值
for key, value in locals().items():
    if key.islower() or key == "URLS":
        continue
    URLS[key] = value

# 拼接完整的URL
for key, host in HOSTS.items():
    url_map = URLS.get(key)
    if url_map is None:
        continue
    for name, url in url_map.items():
        URLS[key][name] = host + url

# 动态注入到当前环境中,可在其他文件from conf.urls import XX使用
sys.modules['conf.urls'] = ObjectDict(URLS)
