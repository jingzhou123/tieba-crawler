#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider

from scrapy import Selector
from urlparse import urlparse, parse_qs
import logging

class UserRelationSpider(CookieSpider, DbSpider):

    """must provide name and request_url_tmpl"""

    def __init__(self):
        """todo: to be defined1. """
        CookieSpider.__init__(self)
        DbSpider.__init__(self)

    def query_some_records(self, start_index = 0, num = 50):
        """todo: docstring for query_some_records.

        :start_index: todo
        :num: todo
        :returns: todo

        """
        cursor = self.conn.cursor()
        # baidu_id: 用户的百度16字节id
        cursor.execute("""
            select baidu_id, name, following_num, followed_num from user limit %s, %s
        """, (
            start_index,
            num
        ))# 去重

        return cursor.fetchall()

    def url_from_row(self, row):
        """todo: docstring for url_from_row.

        :row: todo
        :returns: todo

        """
        return self.request_url_tmpl % (row[0]) # row only has user's baidu_id

    def next_page(self, response):
        """todo: docstring for next_page.

        :response: todo
        :returns: todo

        """
        href = Selector(response).css('.next::attr(href)').extract_first()
        return 'http://tieba.baidu.com' + href if href else False

    def parse_page(self, response):
        """must be implemented to parse a page.

        :response: todo
        :returns: todo

        """
        pass




