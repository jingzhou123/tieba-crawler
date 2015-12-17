#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
import logging

class MemberSpider(CookieSpider, DbSpider):
    """爬一个贴吧的会员，也就是关注这个贴吧的所有人"""
    request_url_tmpl = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=%s&ie=utf-8&pn=%s'
    name = 'member'

    def query_records(self, start_index = 0, num = 50):
        """TODO: Docstring for query_records.

        :start_index: TODO
        :step: TODO
        :returns: TODO

        """
        while True:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT user_name from user_manage_tieba limit %s, %s""", (start_index, num))
            rows = cursor.fetchall()

            if rows:
                for row in rows:
                    yield row

    def url_from_row(self, row):
        return self.request_url_tmpl % (row[0], 1)

    def parse(self, response):
        """TODO: Docstring for parse.

        :response: TODO
        :returns: TODO

        """
        pass


