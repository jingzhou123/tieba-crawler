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

        logging.debug('before parsing next page if existed..')
        meta = response.meta
        next_page = self._get_next_page(response)
        if  next_page > meta['cur_page']: #meta.reply_id meta.post_id
            yield Request(self.request_url_tmpl % (meta['post_id'], meta['reply_id'], next_page),
                    callback=self.parse, meta={'post_id': meta['post_id'], 'reply_id': meta['reply_id'], 'cur_page': next_page}) # tid is 主贴的id, pid是回复的id

    def _get_next_page(self, response):
        """TODO: Docstring for _parse_next_page.

        :response: TODO
        :returns: TODO

        """
        #logging.debug('beginning parsing next page if existed..')
        meta = response.meta
        anchor_sels = Selector(response).css('.j_pager a')
        next_page = 1
        #logging.debug('anchor selectors: %r' % (anchor_sels))
        for sel in anchor_sels:
            #logging.debug('pager anchor text: ' % (sel.css('::text').extract_first()))
            if sel.css('::text').extract_first() == '下一页':
                next_page = sel.css('::attr(href)').extract_first()[1:]
                logging.debug('next page num: %s' % (next_page))

        return int(next_page)


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
                            meta={'post_id': post_id, 'reply_id': reply_id, 'cur_page': 1})

                i = i + step
            else:
                break

