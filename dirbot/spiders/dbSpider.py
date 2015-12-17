from dirbot.settings import MYSQL_HOST, MYSQL_USER, MYSQL_DBNAME, MYSQL_PASSWD
from scrapy.spiders import Spider
from scrapy import Request
import MySQLdb
import logging

class DbSpider(Spider):

    """make spider can query database"""

    def __init__(self):
        """TODO: to be defined1. """
        dbargs = dict(
            host=MYSQL_HOST,
            db=MYSQL_DBNAME,
            user=MYSQL_USER,
            passwd=MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True,
        )
        self.conn = MySQLdb.connect(**dbargs)

    def empty_page(self, response):
        """TODO: Docstring for empty_page.

        :response: TODO
        :returns: TODO

        """
        return False

    def next_page(self, response):
        """TODO: Docstring for next_page.

        :response: TODO
        :returns: TODO

        """
        return False

    def query_some_records(self, start_index = 0, num = 50):
        """TODO: Docstring for query_some_records.

        :start_index: TODO
        :num: TODO
        :returns: TODO

        """
        pass

    def _query_records(self, start_index = 0, step = 50):
        """TODO: Docstring for query_records.
        :returns: yield a row from database, etc user's name

        """
        i = start_index
        while True:
            rows = self.query_some_records(i, step)

            if rows:
                for row in rows:
                    yield row
                i = i + step
            else:
                break

    def url_from_row(self, row):
        """TODO: Docstring for generate_url_from_row.
        :returns: TODO

        """
        pass

    def start_requests(self):
        """TODO: Docstring for start_requests.
        :returns: TODO

        """

        for row in self._query_records():
            yield Request(self.url_from_row(row), callback=self.parse, meta={'row': row}) # do something with rows from database

    def parse(self, response):
        """TODO: Docstring for parse.

        :response: TODO
        :returns: TODO

        """

        if self.empty_page(response):
            return

        for item in self.parse_page(response):
            yield item

        next_page_url = self.next_page(response)
        if next_page_url:
            yield Request(next_page_url, callback=self.parse_page, meta={'row': response.meta['row']})




