from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import logging

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
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _do_upsert(self, conn, item, spider):
        """Perform an insert or update."""
        conn.execute("""SELECT EXISTS(
            SELECT name FROM tieba WHERE name = %s
        )""", (item['name'], ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE tieba
                SET followed_num=%s, belong_dir=%s, slogan=%s, posts_num=%s
                WHERE name=%s
            """, (item['members_num'], item['dir_name'], item['slogan'], item['posts_num'], item['name'], ))
            spider.log("Item updated in db: %s %r" % (item['name'], item))
        else:
            conn.execute("""
                INSERT INTO tieba VALUES (DEFAULT, %s, %s, DEFAULT, %s, %s, %s)
            """, (
                item['name'], item['members_num'], item['posts_num'], item['slogan'], item['dir_name'],
            ))

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.error(failure)
