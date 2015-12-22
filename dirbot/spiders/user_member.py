#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from dirbot.items import User

from scrapy import Request, Selector
from urlparse import urlparse, parse_qs
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
        cursor.execute("""
            SELECT DISTINCT user_name from user_follow_tieba limit %s, %s
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
        return self.request_url_tmpl % (row[0]) # row only has user's name

    def parse_page(self, response):
        """TODO: Docstring for parse_page.

        :response: TODO
        :returns: TODO

        """
        item = User()
        item['tieba_age'] = self._parse_user_age(response)
        item['posts_num'] = self._parse_user_posts_num(response)
        item['following_tieba_name_array'] = self._parse_user_following_tieba(response)
        item['name'] = response.meta['row'][0]
        item['baidu_id'] = self._parse_user_id(response)
        item = self._parse_following_and_followed(response, item)

        yield item

    def _parse_user_id(self, response):
        """TODO: Docstring for _parse_user_id.

        :response: TODO
        :returns: 32 digits user id hex

        """

        uri = Selector(response).css('.concern_num a::attr(href)').extract_first()
        logging.debug('user id href: %s' % (uri))
        if uri:
            query_dict = parse_qs(urlparse(uri).query)
            # uri maybe this: /home/concern?id=a3e3474fbda1bfb5bfecc0d6d121?t=1423636759&fr=home
            return query_dict['id'][0]
        else:
            return ''

    def _parse_following_and_followed(self, response, item):
        """TODO: Docstring for _parse_following_and_followed.

        :response: TODO
        :item: item.following_num item.followed_num
        :returns: TODO

        """
        sels = Selector(response).css('.ihome_aside_title')
        for sel in sels:
            title = sel.css('::text').extract_first().strip()# 第一个text是'他关注的人'或者其它无用的信息
            #logging.debug('title: %s' % (title))
            #有的用户没有关注或被关注
            if title == '他关注的人' or title == '她关注的人':
                item['following_num'] = sel.css('a::text').extract_first()
            else:
                item['following_num'] = 0
            if title == '关注他的人' or title == '关注她的人':
                item['followed_num'] = sel.css('a::text').extract_first()
            else:
                item['followed_num'] = 0

        return item


    def _parse_user_following_tieba(self, response):
        """TODO: Docstring for _parse_user_following_tieba.

        :response: TODO
        :returns: TODO

        """
        names = []
        for name in Selector(response).css('.u-f-item span:first-child::text').extract():
            names.append(name)

        return names


    def _parse_user_age(self, response):
        """TODO: Docstring for _parse_user_age.

        :response: TODO
        :returns: TODO

        """

        return Selector(response).css('.userinfo_userdata span:nth-child(2)::text').extract_first()[3:-1] or 0# 吧龄:(X)X.X年

    def _parse_user_posts_num(self, response):
        """TODO: Docstring for _parse_user_posts_num.

        :response: TODO
        :returns: TODO

        """
        num = Selector(response).css('.userinfo_userdata span:nth-child(4)::text').extract_first()[3:-1]# 发贴:(X)X.X万
        logging.debug('posts num: %s' % (num))
        if num:
            return num if num.find('.') != -1 else float(num) * 10000
        else:
            return 0

