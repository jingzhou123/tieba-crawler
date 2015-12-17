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
    def get_query_sql(self):
        """TODO: Docstring for get_query_sql.
        :returns: TODO

        """
        pass

    def query_records(self, start_index = 0, step = 50):
        """TODO: Docstring for query_records.
        :returns: yield a row from database, etc user's name

        """


    def url_from_row(self, row):
        """TODO: Docstring for generate_url_from_row.
        :returns: TODO

        """
        pass

    def start_requests(self):
        """TODO: Docstring for start_requests.
        :returns: TODO

        """

        for row in self.query_records():
            yield Request(self.url_from_row(row), callback=self.parse, meta={'row': row}) # do something with rows from database




