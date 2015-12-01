#coding=utf-8
import scrapy
from cookieSpider import CookieSpider as Spider
from scrapy.selector import Selector

from dirbot.items import Tieba

class TiebaSpider(Spider):
    name= "tieba"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/bawu2/platform/detailsInfo?ie=utf-8&word=北京邮电大学"
    ]#TODO:动态地生成一个list

    def parse_owners(self, response):
        sel = Selector(response)
        return sel.css('.bawu_single_type.first_section a.user_name::text').extract()#吧主
#TODO: 小吧主，图片吧务

    def parse_name(self, response):
        sel = Selector(response)
        return sel.css('.card_title_fname::text').extract()[0].strip()

    def parse(self, response):
        """TODO: Docstring for parse.
        :returns: TODO

        """
        items = []
        item = Tieba()
        item['owners'] = self.parse_owners(response)
        item['name'] = self.parse_name(response)
        items.append(item)

        return items


