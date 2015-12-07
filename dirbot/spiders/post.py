#coding=utf-8
from scrapy import Request
from cookieSpider import CookieSpider as Spider
from scrapy.selector import Selector
from dirbot.settings import TIEBA_NAMES_LIST
from dirbot.items import Post
import logging

class PostSpider(Spider):

    """Docstring for PostSpider. """

    name = 'post'
    allowed_domains = ["baidu.com"]

    def start_requests(self):
        """TODO: Docstring for start_requests.
        :returns: TODO

        """
        url_list = map(
            lambda name: ("http://tieba.baidu.com/f?ie=utf-8&kw=" + name),
            TIEBA_NAMES_LIST
        )

        for url in url_list:
            yield Request(url, callback=self.parse)
    def _parse_posts(self, response):
        """TODO: Docstring for _parse_posts.

        :response: TODO
        :returns: TODO

        """
        item = Post()
        item['id'] = 123

        yield item

    def parse(self, response):
        """TODO: Docstring for pass.

        :response: TODO
        :returns: TODO

        """
        self._parse_posts(response)

        logging.debug('length: %s' % (len(Selector(response).css('.next pagination'))))
        if len(Selector(response).css('.next.pagination-item')):
            logging.debug('iterating..')
            yield Request(Selector(response).css('.next.pagination-item::attr(href)').extract_first(), callback=self.parse)

