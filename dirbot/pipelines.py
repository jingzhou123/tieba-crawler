from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi

class TiebaPipeline(object):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    code below is referred from
    'https://github.com/rolando/dirbot-mysql/blob/master/dirbot/pipelines.py'
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
        return item
