#coding=utf-8
from scrapy import Request
from cookieSpider import CookieSpider as Spider
from dirbot.settings import TIEBA_NAMES_LIST

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

    def parse(self, response):
        """TODO: Docstring for pass.

        :response: TODO
        :returns: TODO

        """
        pass

