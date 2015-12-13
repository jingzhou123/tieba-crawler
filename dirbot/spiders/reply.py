#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request
import logging

class ReplySpider(CookieSpider, DbSpider):

    """a spider for crawling the post's replies and replies' replies"""
    name = 'reply'

    def _query_posts(self, start_index, num):
        """TODO: Docstring for _query_posts.
        :returns: TODO

        """

        cursor = self.conn.cursor()
        cursor.execute("""SELECT id from post limit %s, %s""", (start_index, num));
        return cursor.fetchall()

    def start_requests(self):
        """entry for generating all requests
        :returns: TODO

        """
        try:
            i = 0
            while True:
                rows = self._query_posts(i, 50)
                if rows:
                    for row in rows:
                        logging.debug("an post's id: %r" % row[0])
                        yield Request('http://tieba.baidu.com/p/' + str(row[0]), callback=self.parse)
                    i = i + 50
                else:
                    break
        except Exception, e:
            raise e

    def parse(self, response):
        """TODO: Docstring for parse.
        :returns: TODO

        """
        pass



