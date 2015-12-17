#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import UserFollowTiebaRel
import logging
import json

class UserMemberSpider(CookieSpider, DbSpider):

    """Docstring for UserSpider. """
    name = 'user_member'# 命名规则 user_{从哪种渠道获得的用户名称}
    request_url_tmpl = 'http://tieba.baidu.com/home/main?un=%s&ie=utf-8'

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
        cursor.execute("""SELECT user_name from user_follow_tieba limit %s, %s""", (start_index, num))
        return cursor.fetchall()

    def url_from_row(self, row):
        """TODO: Docstring for url_from_row.

        :row: TODO
        :returns: TODO

        """
        return self.request_url_tmpl % (row[0]) # row only has user's name

    def parse_page(self, response):
        """TODO: Docstring for parse_page.

        :response: TODO
        :returns: TODO

        """
        yield 'user'


