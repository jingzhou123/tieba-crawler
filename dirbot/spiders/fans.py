#coding=utf-8

from user_relation import UserRelationSpider
from dirbot.items import Fan

from scrapy import Request, Selector
from urlparse import urlparse, parse_qs
import logging

class FanSpider(UserRelationSpider):

    """docstring for fanspider. """
    name = 'fan'
    request_url_tmpl = 'http://tieba.baidu.com/home/fans?id=%s&fr=home'

    def should_go(self, row):
        """TODO: Docstring for should_go.

        :row: TODO
        :returns: TODO

        """
        return row[3] != 0

    def parse_page(self, response):
        """todo: docstring for parse_page.

        :response: todo
        :returns: todo

        """
        logging.debug('fans num: %s' % (len(Selector(response).css('.user'))))
        for sel in Selector(response).css('.user'):
            item = Fan()
            item['name'] = sel.css('.name a::text').extract_first()
            item['baidu_id'] = sel.css('::attr(portrait)').extract_first()
            item['user_name_followed'] = response.meta['row'][1]# 是谁的粉丝

            yield item




