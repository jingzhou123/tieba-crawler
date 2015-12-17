#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
import logging

class MemberSpider(CookieSpider, DbSpider):
    """爬一个贴吧的会员，也就是关注这个贴吧的所有人"""
    request_url_tmpl = 'http://tieba.baidu.com/bawu2/platform/listMemberInfo?word=%s&ie=utf-8&pn=%s'
    name = 'member'

    def start_requests(self):
        """TODO: Docstring for start_requests.
        :returns: TODO

        """
        pass
