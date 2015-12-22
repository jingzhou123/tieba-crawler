#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from dirbot.items import Fan

from scrapy import Request, Selector
from urlparse import urlparse, parse_qs
import logging

class FanSpider(CookieSpider, DbSpider):

    """Docstring for FanSpider. """
    name = 'fan'
    request_url_tmpl = 'http://tieba.baidu.com/home/fans?id=%s&fr=home'

    def __init__(self):
        """TODO: to be defined1. """
        CookieSpider.__init__(self)
        DbSpider.__init__(self)

    def query_some_records(self, start_index = 0, num = 50):
        """TODO: Docstring for query_some_records.

        :start_index: TODO
        :num: TODO
        :returns: TODO

        """
        cursor = self.conn.cursor()
        # baidu_id: 用户的百度16字节id
        cursor.execute("""
            SELECT baidu_id from user limit %s, %s
        """, (
            start_index,
            num
        ))# 去重

        return cursor.fetchall()

    def url_from_row(self, row):
        """TODO: Docstring for url_from_row.

        :row: TODO
        :returns: TODO

        """
        return self.request_url_tmpl % (row[0]) # row only has user's baidu_id

    def next_page(self, response):
        """TODO: Docstring for next_page.

        :response: TODO
        :returns: TODO

        """
        href = Selector(response).css('.next::attr(href)').extract_first()
        return 'http://tieba.baidu.com' + href if href else False

    def parse_page(self, response):
        """TODO: Docstring for parse_page.

        :response: TODO
        :returns: TODO

        """
        logging.debug('fans num: %s' % (len(Selector(response).css('.user'))))
        for sel in Selector(response).css('.user'):
            item = Fan()
            item['name'] = sel.css('.name a::text').extract_first()
            item['baidu_id'] = sel.css('::attr(portrait)').extract_first()

            yield item




