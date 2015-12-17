#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import UserFollowTiebaRel
import logging

class MemberSpider(CookieSpider, DbSpider):
    """爬一个贴吧的会员，也就是关注这个贴吧的所有人"""
    request_url_tmpl = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=%s&ie=utf-8&pn=%s'
    name = 'member'

    def query_some_records(self, start_index = 0, num = 50):
        """TODO: Docstring for query_records.

        :start_index: TODO
        :step: TODO
        :returns: TODO

        """
        cursor = self.conn.cursor()
        cursor.execute("""SELECT name from tieba limit %s, %s""", (start_index, num))
        return cursor.fetchall()

    def url_from_row(self, row):
        return self.request_url_tmpl % (row[0], 1)

    def next_page(self, response):
        """TODO: Docstring for next_page.

        :response: TODO
        :returns: TODO

        """
        return 'http://tieba.baidu.com' + Selector(response).css('.next_page::attr(href)').extract_first()

    def empty_page(self, response):
        """TODO: Docstring for empty_page.

        :response: TODO
        :returns: TODO

        """
        return False

    def parse_page(self, response):
        """TODO: Docstring for parse.

        :response: TODO
        :returns: TODO

        """

        items = []
        for user_name in Selector(response).css('.user_name::attr(title)').extract():
            item = UserFollowTiebaRel()
            item['user_name'] = user_name
            item['tieba_name'] = response.meta['row'][0] #tieba_name
            #logging.debug('meta: %r' % (response.meta))
            items.append(item)

        return items


