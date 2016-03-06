# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from fang_price.items import FangPriceItem
from fang_price.lib import utils


class FangPrice(scrapy.Spider):
    """
    fang_price
    """

    name = "fang_price"
    allowed_domains = ["fang.com"]
    start_urls = "http://newhouse.lf.fang.com/house/s/b9{0}/"

    def start_requests(self):
        for index in range(1, 41):
            path = self.start_urls.format(index)
            yield self.make_requests_from_url(path)

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select(
            u".//*[@id='bx1']//node()/div[@class='nl_con clearfix']/ul/li//node()/div[@class='nlcd_name']/a[1]/@href"
        ).extract()
        if urls:
            for url in urls:
                # time.sleep(1)
                yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        """
        列表
        :param response:
        :return:
        """
        hxs = HtmlXPathSelector(response)
        f = FangPriceItem()
        f["page_url"] = response.url
        f["page_resp"] = response.body.decode(response.encoding)
        f["fang_title"] = utils.join_and_wash("", hxs.select(u".//h1/a[1]/text()").extract())
        f["avg_price"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='information']//node()/p/strong[contains(text(), '平均价格')]/../span/text()"
        ).extract())
        f["user_score"] = utils.join_and_wash("-", hxs.select(
            u".//*[@id='xfptxq_B04_08']/div[@class='inf_right fl']/div//node()/text()"
        ).extract())
        f["lasted_open"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='information']//node()/p/strong[contains(text(), '最新开盘')]/../a/text()"
        ).extract())
        f["address"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='information']//node()/p/strong[contains(text(), '楼盘地址')]/../span/text()"
        ).extract())
        f["main_unit"] = utils.join_and_wash("-", hxs.select(
            u".//div[@class='information']//node()/p/strong[contains(text(), '主力户型')]/../a/text()"
        ).extract())

        f["detail_url"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='fl more']/p/a[@id='xfptxq_B04_14']/@href"
            u"| .//div[@class='fl more']/p/a[@id='xfptxq_B04_13']/@href"
        ).extract())
        yield f
        if f["detail_url"]:
            # time.sleep(1)
            yield Request(f["detail_url"], callback=self.prase_detail)

    def prase_detail(self, response):
        """
        prase_detail
        :return:
        """
        hxs = HtmlXPathSelector(response)
        f = FangPriceItem()
        f["detail_url"] = response.url
        f["detail_resp"] = response.body.decode(response.encoding)
        f["property_type"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '物业类别')]/../text()"
        ).extract())
        f["advantage"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '项目特色')]/../text()"
        ).extract())
        f["construction_type"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '建筑类别')]/../text()"
        ).extract())
        f["decoration_status"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '装修状况')]/../text()"
        ).extract())
        f["loop_position"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '环线位置')]/../text()"
        ).extract())
        f["trading_area"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '所属商圈')]/../text()"
        ).extract())
        f["volume_ratio"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '容 积 率')]/../text()"
        ).extract())
        f["greening_rate"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '绿 化 率')]/../text()"
        ).extract())
        f["open_date"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '开盘时间')]/../text()"
        ).extract())
        f["launch_date"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '交房时间')]/../text()"
        ).extract())
        f["property_fee"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '物 业 费')]/../text()"
        ).extract())
        f["property_company"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '物业公司')]/../text()"
        ).extract())
        f["open_dealer"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '开 发 商')]/../text()"
        ).extract())
        f["sales_address"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '售楼地址')]/../text()"
        ).extract())
        f["property_address"] = utils.join_and_wash("", hxs.select(
            u".//div[@class='besic_inform']/table//td/strong[contains(text(), '物业地址')]/../text()"
        ).extract())
        f["traffic"] = utils.join_and_wash("", hxs.select(
            u".//h2[contains(text(), '交通状况')]/following-sibling::*[1]/text()"
        ).extract())
        f["supporting_projects"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '项目配套')]/following-sibling::*[1]/text()"
        ).extract())
        f["building_decoration"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '建材装修')]/following-sibling::*[1]/text()"
        ).extract())
        f["floor_condition"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '楼层状况')]/following-sibling::*[1]/text()"
        ).extract())
        f["parking_information"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '车位信息')]/following-sibling::*[1]/text()"
        ).extract())
        f["introduction"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '项目简介')]/following-sibling::*[1]/text()"
        ).extract())
        f["related_information"] = utils.join_and_wash("-", hxs.select(
            u".//h2[contains(text(), '相关信息')]/following-sibling::*[1]/text()"
        ).extract())

        price_info = hxs.select(u".//*[@id='priceListOpen']/table//tr[position()>1]/td").extract()
        price_info = [
            val.replace('<td>', '').replace('</td>', '').replace(u'\xa0', '').replace('<td class="payDescription">', '')
            for val in price_info
        ]
        f["price_info"] = price_info
        yield f
