# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from fang_price.db import mixin


class FangPriceItem(scrapy.Item, mixin.Mixin):
    """

    """
    page_url = scrapy.Field()  # 页面地址
    page_resp = scrapy.Field()  # 页面内容
    fang_title = scrapy.Field()  # 房产名称
    avg_price = scrapy.Field()  # 平均价格
    user_score = scrapy.Field()  # 用户评分
    lasted_open = scrapy.Field()  # 开盘时间
    address = scrapy.Field()  # 楼盘地址
    main_unit = scrapy.Field()  # 主力户型

    detail_url = scrapy.Field()  # 详情页地址
    detail_resp = scrapy.Field()  # 详情页内容
    property_type = scrapy.Field()  # 物业类别
    advantage = scrapy.Field()  # 特色项目
    construction_type = scrapy.Field()  # 建筑类别
    decoration_status = scrapy.Field()  # 装修状况
    loop_position = scrapy.Field()  # 环线位置
    trading_area = scrapy.Field()  # 商圈
    volume_ratio = scrapy.Field()  # 容积率
    greening_rate = scrapy.Field()  # 绿化率
    open_date = scrapy.Field()  # 开盘时间
    launch_date = scrapy.Field()  # 交房时间
    property_fee = scrapy.Field()  # 物业费
    property_company = scrapy.Field()  # 物业公司
    open_dealer = scrapy.Field()  # 开发商
    sales_address = scrapy.Field()  # 售楼地址
    property_address = scrapy.Field()  # 物业地址
    traffic = scrapy.Field()  # 交通状况

    supporting_projects = scrapy.Field()  # 项目配套
    building_decoration = scrapy.Field()  # 建材装修
    floor_condition = scrapy.Field()  # 楼层状况
    parking_information = scrapy.Field()  # 车位信息
    introduction = scrapy.Field()  # 项目简介
    related_information = scrapy.Field()  # 相关信息

    price_info = scrapy.Field()  # 房价信息
