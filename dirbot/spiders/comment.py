#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import Comment
import json
import logging

class CommentSpider(CookieSpider, DbSpider):

    """crawl a post's reply's comments"""
    request_url_tmpl = 'http://tieba.baidu.com/p/comment?tid=%s&pid=%s&pn=%s'
    name = 'comment'

    def _query_replies(self, start_index, num):
        """

        :start_index: TODO
        :num: TODO
        :returns: TODO

        """
        cursor = self.conn.cursor()
        cursor.execute("""SELECT id, post_id from reply limit %s, %s""", (start_index, num))
        return cursor.fetchall()

    def _parse_page(self, response):
        """TODO: Docstring for _parse_page.

        :response: TODO
        :returns: TODO

        """

    def parse(self, response):
        """TODO: Docstring for parse.

        :response: TODO
        :returns: TODO

        """

        replies_sel = Selector(response).css('.lzl_single_post')
        for sel in replies_sel:
            item = Comment()
            item['body'] = ''.join(sel.css('.lzl_content_main::text').extract()).strip()
            comment_json_str = sel.css('::attr(data-field)').extract_first()
            comment_json = json.loads(comment_json_str)
            item['id'] = comment_json['spid']# 直接取百度的id
            item['author_name'] = comment_json['user_name']
            item['post_time'] = self._fill_time(sel.css('.lzl_time::text').extract_first())
            item['reply_id'] = response.meta['reply_id']
            logging.debug('comment: %r' % (item))
            yield item

        self._parse_next_page(response)

    def _parse_next_page(self, response):
        """TODO: Docstring for _parse_next_page.

        :response: TODO
        :returns: TODO

        """

    def _fill_time(self, time):
        """TODO: Docstring for _fill_time.

        :time: 1111-11-11 11:11:11 or 1111-11-11
        :returns: TODO

        """
        if len(time) <= len('YYYY-MM-DD'):
            return  time + ' 00:00:00'
        else:
            return time

    def start_requests(self):
        """TODO: Docstring for start_requests.
        :returns: TODO

        """
        i = 0
        page = 1
        step = 50
        while True:
            rows = self._query_replies(i, step)
            if rows:
                for row in rows:
                    reply_id = row[0]
                    post_id = row[1]
                    yield Request(self.request_url_tmpl % (post_id, reply_id, 1), # tid is 主贴的id, pid是回复的id
                            callback=self.parse,
                            meta={'post_id': post_id, 'reply_id': reply_id})

                i = i + step
            else:
                break

