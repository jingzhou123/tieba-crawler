#coding=utf-8

from user_relation import UserRelationSpider
from dirbot.items import Follow

from scrapy import Request, Selector
from urlparse import urlparse, parse_qs
import logging

class FollowSpider(UserRelationSpider):

    """爬取用户关注的用户"""
    name = 'follow'
    request_url_tmpl = 'http://tieba.baidu.com/home/concern?id=%s&fr=home'

    def should_go(self, row):
        """TODO: Docstring for should_go.

        :row: TODO
        :returns: TODO

        """
        return row[2] != 0

    def parse_page(self, response):
        """todo: docstring for parse_page.

        :response: todo
        :returns: todo

        """
        for sel in Selector(response).css('.user'):
            item = Follow()
            item['name'] = sel.css('.name a::text').extract_first()
            item['baidu_id'] = sel.css('::attr(portrait)').extract_first()
            item['user_name_following'] = response.meta['row'][1]# 是被谁关注的

            yield item




