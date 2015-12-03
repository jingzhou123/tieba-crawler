#coding=utf-8
import scrapy
import re
import logging
from scrapy import Request
from cookieSpider import CookieSpider as Spider
from scrapy.selector import Selector
from dirbot.items import Tieba
from dirbot.settings import TIEBA_NAMES_LIST

class TiebaSpider(Spider):
    name= "tieba"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/bawu2/platform/listBawuTeamInfo?ie=utf-8&word=北京邮电大学",
        "http://tieba.baidu.com/bawu2/platform/listBawuTeamInfo?ie=utf-8&word=北京师范大学",
    ]#TODO:动态地生成一个list

    def _to_int(self, numstr):
        """TODO: Docstring for _to_int.

        :num: a string like '403,000'
        :returns: 403000

        """
        return int(re.sub(',', '', numstr));

    def parse_admin_num(self, response):
        """TODO: Docstring for parse_admin_num.
        :returns: TODO

        """
        sel = Selector(response)
        return len(sel.css('.user_name').extract())#职业吧主+吧主+小吧主+图片。。。

    def parse_name(self, response):
        sel = Selector(response)
        return sel.css('.card_title_fname::text').extract()[0].strip()

    def parse_slogan(self, response):
        """TODO: Docstring for parse_card_slogan.

        :response: TODO
        :returns: TODO

        """
        sel = Selector(response)
        try:
            return sel.css('.card_slogan::text').extract()[0].strip()
        except Exception, e:
            return ''


    def parse_members_num(self, response):
        """TODO: Docstring for parse_members_num.

        :response: TODO
        :returns: TODO

        """
        sel = Selector(response)
        try:
            return self._to_int(sel.css('.card_menNum::text').extract()[0].strip()) # format: 40,876
        except:
            return 0

    def parse_posts_num(self, response):
        """TODO: Docstring for parse_posts_num.

        :arg1: TODO
        :returns: TODO

        """
        sel = Selector(response)
        try:
            return self._to_int(sel.css('.card_infoNum::text').extract()[0].strip()) # format: 40,876
        except:
            return 0

    def parse_dir_name(self, response):
        """TODO: Docstring for parse_dir_name.

        :response: TODO
        :returns: TODO

        """
        sel = Selector(response)
        return sel.css('.forum_dir_info li:last-child a::text').extract()[0].strip() # format: 40,876

    def start_requests(self):
        """scrapy interface
        :returns: TODO

        """
        urls_list = map(
                lambda name: ("http://tieba.baidu.com/bawu2/platform/listBawuTeamInfo?ie=utf-8&word=" + name),
                TIEBA_NAMES_LIST)

        for url in urls_list:
            yield scrapy.Request(url, callback=self.parse_all)

    def parse_all(self, response):
        """TODO: Docstring for parse.
        :returns: TODO

        """
        items = []
        item = Tieba()
        item['admin_num'] = self.parse_admin_num(response)
        item['name'] = self.parse_name(response)
        item['members_num'] = self.parse_members_num(response)
        item['posts_num'] = self.parse_posts_num(response)
        item['slogan'] = self.parse_slogan(response)
        item['dir_name'] = self.parse_dir_name(response)
        items.append(item)

        return items



