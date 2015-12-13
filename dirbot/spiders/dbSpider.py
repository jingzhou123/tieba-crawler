from dirbot.settings import MYSQL_HOST, MYSQL_USER, MYSQL_DBNAME, MYSQL_PASSWD
from scrapy.spiders import Spider
import MySQLdb

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


