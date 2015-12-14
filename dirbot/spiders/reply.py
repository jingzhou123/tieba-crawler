#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import Reply
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

    def _has_comments(self, post):
        """TODO: Docstring for _has_comments.

        :post: TODO
        :returns: TODO

        """
        pass

    def _parse_reply(self, post):
        """TODO: Docstring for _parse_reply.

        :post: TODO
        :returns: TODO

        """
        pass

    def _parse_comments(self, post):
        """TODO: Docstring for _parse_comments.

        :post: TODO
        :returns: TODO

        """
        pass

    def _fill_time(self, time):
        """TODO: Docstring for _fill_time.

        :time: 1111-11-11 11:11:11 or 1111-11-11
        :returns: TODO

        """
        if len(time) <= len('YYYY-MM-DD'):
            return  time + ' 00:00:00'
        else:
            return time

    def _parse_main_post(self, post, response):
        """TODO: Docstring for _parse_main_post.

        :post: TODO
        :returns: TODO

        """
        item = Reply()
        item['type'] = 'MAIN'
        #拼接字符串
        item['body'] = ''.join(post.css('cc div::text').extract()).strip()
        item['title'] = Selector(response).css('h3.core_title_txt::text').extract_first()
        item['post_time'] = self._fill_time(post.css('.post-tail-wrap span.tail-info:last-child::text').extract_first())
        item['id'] = response.meta['post_id']
        #TODO: time

        return item;

    def start_requests(self):
        """entry for generating all requests
        :returns: TODO

        """
        """
        try:
            i = 0
            while True:
                rows = self._query_posts(i, 50)
                if rows:
                    for row in rows:
                        logging.debug("an post's id: %r" % row[0])
                        post_id = str(row[0])
                        yield Request('http://tieba.baidu.com/p/' + post_id, callback=self.parse, meta={'post_id': post_id})
                    i = i + 50
                else:
                    break
        except Exception, e:
            raise e
        """
        yield Request('http://tieba.baidu.com/p/' + '4191511745', callback=self.parse, meta={'post_id': 4191511745})

    def parse(self, response):
        """TODO: Docstring for parse.
        :returns: TODO

        """
        posts = Selector(response).css('.p_postlist .l_post')
        logging.debug('posts num: %s', len(posts))

        for i, post in enumerate(posts):
            if i == 0:
                logging.debug('main post: %r', self._parse_main_post(post, response))
                yield self._parse_main_post(post, response)
            #else:
            #    yield self._parse_reply(post)

            #if self._has_comments(post):
            #    self._parse_comments(post)





