#coding=utf-8

from dirbot.items import User
from user import UserSpider

from scrapy import Request, Selector
from urlparse import urlparse, parse_qs
import logging
import json

class UserFollowSpider(UserSpider):

    """Docstring for UserSpider. """
    name = 'user_follow'# 命名规则 user_{从哪种渠道获得的用户名称}

    def query_some_records(self, start_index = 0, num = 50):
        """TODO: Docstring for query_some_records.

        :start_index: TODO
        :num: TODO
        :returns: TODO

        """

        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name from follow limit %s, %s
        """, (
            start_index,
            num
        ))# 去重
        return cursor.fetchall()
