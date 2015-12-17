#coding=utf-8
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import logging

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TbBasePipeline(object):
    """docstring for TbBasePipeline"""
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def noop(self):
        pass

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.error(failure)

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

class TiebaPipeline(TbBasePipeline):
    """A pipeline to store the item in a MySQL database.
    This implementation uses Twisted's asynchronous database API.
    code below is referred from
    'https://github.com/rolando/dirbot-mysql/blob/master/dirbot/pipelines.py'
    """

    def process_item(self, item, spider):
        if spider.name != 'tieba':
            d = self.dbpool.runInteraction(self.noop, item, spider)
            d.addBoth(lambda _: item)
            return d

        logging.debug('processing tieba: %r' % (item))
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _insert_tieba_admins(self, conn, item, spider):
        """TODO: INSERT IGNORE ...

        :conn: TODO
        :item: TODO
        :spider: TODO
        :returns: TODO
        """

        for name in item['admin_names']:
            #logging.debug("(%s, %s)" % (name, item['name'])); #right
            #logging.debug('%s' % (type(name))) #unicode
            conn.execute("""
                INSERT user_manage_tieba VALUES(%s, %s)
                ON DUPLICATE KEY UPDATE user_name=%s, tieba_name=%s
            """, (name, item['name'], name, item['name']))

    def _do_upsert(self, conn, item, spider):
        logging.debug('processing item from posts..')
        """Perform an insert or update."""
        conn.execute("""SELECT EXISTS(
            SELECT name FROM tieba WHERE name = %s
        )""", (item['name'], ))
        ret = conn.fetchone()[0]

        if ret:
            conn.execute("""
                UPDATE tieba
                SET followed_num=%s, belong_dir=%s, slogan=%s, posts_num=%s,admin_num=%s
                WHERE name=%s
            """, (item['members_num'], item['dir_name'], item['slogan'],
                item['posts_num'], item['admin_num'], item['name'], ))
        else:
            conn.execute("""
                INSERT INTO tieba VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)
            """, (
                item['name'], item['members_num'], item['admin_num'],
                item['posts_num'], item['slogan'], item['dir_name'],
            ))

        self._insert_tieba_admins(conn, item, spider);

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.error(failure)

class PostPipeline(TbBasePipeline):

    """Docstring for PostPipeline. """
    def process_item(self, item, spider):
        """TODO: Docstring for process_item.

        :item: TODO
        :returns: TODO

        """
        if spider.name != 'post':
            d = self.dbpool.runInteraction(self.noop, item, spider)
            d.addBoth(lambda _: item)
            return d

        logging.debug('processing post: %r' % (item))
        # run db query in the thread pool
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)
        # return the deferred instead the item. This makes the engine to
        # process next item (according to CONCURRENT_ITEMS setting) after this
        # operation (deferred) has finished.
        return d

    def _fill_in_data(self, item):
        """TODO: Docstring for _fill_in_data.

        :item: TODO
        :returns: TODO

        """
        item['id'] = int(item['id'])
        item['reply_num'] = int(item['reply_num'])
        item['post_time'] = '1970-1-1'# shim data

        return item

    def _do_upsert(self, conn, item, spider):
        """TODO: Docstring for _do_upsert.
        :returns: TODO

        """
        #logging.debug('filtering ads...')
        #logging.debug('post: %r' % (item))
        if item['id'] == '-1':#广告贴
            return
        logging.debug('filtered ads...')

        item = self._fill_in_data(item)
        conn.execute(
            """INSERT INTO post values(%s, %s, %s, %s, %s, %s, %s)
               ON DUPLICATE KEY UPDATE author_name=%s, tieba_name=%s, title=%s, body=%s, post_time=%s, reply_num=%s""",
            (
                item['id'], item['author_name'], item['tieba_name'], item['title'], item['body'], item['post_time'], item['reply_num'],
                #values to update
                item['author_name'], item['tieba_name'], item['title'], item['body'], item['post_time'], item['reply_num']
            )
        )

    def _handle_error(self, failure, item, spider):
        """Handle occurred on db interaction."""
        # do nothing, just log
        logging.error(failure)

class ReplyPipeline(TbBasePipeline):

    """Docstring for ReplyPipeline. """

    def _do_upsert(self, conn, item, spider):
        """TODO: Docstring for _do_update.

        :item: TODO
        :spider: TODO
        :returns: TODO

        """
        if item['type'] == 'MAIN':
            #conn.execute("""UPDATE post SET title=%s, body=%s, post_time=%s where id=%s""", (item['title'], item['body'], item['post_time'], item['id']))
            pass
        else:
            logging.debug('item id: %s' % (item['id']))
            #conn.execute("""INSERT INTO reply SET title=%s, author_name=%s, body=%s, post_time=%s, id=%s, post_id=%s""", (item['title'], item['author_name'], item['body'], item['post_time'], item['id'], item['post_id']))
            #logging.debug("""INSERT INTO reply values(%s, %s, %s, %s, %s, %s, %s, %s)""" % (item['author_name'], item['body'], item['id'], '天', item['title'], item['post_time'], item['post_id'], ''))
            conn.execute("""INSERT INTO reply values(%s, %s, %s, %s, %s, %s, %s)""", (item['author_name'], item['body'], item['id'], item['title'], item['post_time'], item['post_id'], item['reply_num']))

    def process_item(self, item, spider):
        if spider.name != 'reply':
            d = self.dbpool.runInteraction(self.noop, item, spider)
            d.addBoth(lambda _: item)
            return d

        logging.debug('processing reply: %r' % (item))
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)

        return d

class CommentPipeline(TbBasePipeline):
    """Docstring for CommentPipeline. """

    def _do_upsert(self, conn, item, spider):
        """TODO: Docstring for _do_upsert.
        :returns: TODO

        """
        logging.debug('item inserted: %r' % (item))

        conn.execute("""
            INSERT comment VALUES(%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE id=%s, reply_id=%s, author_name=%s, body=%s, post_time=%s
        """, (
            item['id'], item['reply_id'], item['author_name'], item['body'], item['post_time'],
            item['id'], item['reply_id'], item['author_name'], item['body'], item['post_time']
        ))

    def process_item(self, item, spider):
        """TODO: Docstring for process_item.

        :item: TODO
        :spider: TODO
        :returns: TODO

        """
        if spider.name != 'comment':
            d = self.dbpool.runInteraction(self.noop, item, spider)
            d.addBoth(lambda _: item)
            return d

        #logging.debug('processing comment: %r' % (item))
        d = self.dbpool.runInteraction(self._do_upsert, item, spider)
        d.addErrback(self._handle_error, item, spider)
        # at the end return the item in case of success or failure
        d.addBoth(lambda _: item)

        return d


