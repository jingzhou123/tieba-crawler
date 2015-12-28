#coding=utf-8

from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import Reply
import logging
import json
from uuid import uuid1 as uuid

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

    def _parse_reply_num(self, post):
        """提取一个主贴的回复的评论数

        :post: TODO
        :returns: TODO

        """
        #return this "{"total_num": null_or_num}"
        json_str = post.css('div.p_reply::attr(data-field)').extract_first()
        #有的并没有这个div
        return (json_str and json.loads(json_str)['total_num']) or 0

    def _parse_reply(self, post, response):
        """TODO: Docstring for _parse_reply.

        :post: TODO
        :returns: TODO

        """
        item = self._parse_general_post(post, response)
        #item['id'] = str(uuid().int>>64)[0:16]
        item['id'] = json.loads(post.css('::attr(data-field)').extract_first())['content']['post_id']# 百度给出的一条评论的id
        item['post_id'] = response.meta['post_id']
        item['author_name'] = post.css('.d_name a::text').extract_first()
        item['type'] = None
        item['reply_num'] = self._parse_reply_num(post)

        return item

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
        if time and len(time) <= len('YYYY-MM-DD'):
            return  time + ' 00:00:00'
        else:
            return time

    def _parse_general_post(self, post, response):
        """TODO: Docstring for _parse_general_post.

        :post: TODO
        :response: TODO
        :returns: TODO

        """
        item = Reply()
        #拼接字符串
        item['body'] = ''.join(post.css('cc div::text').extract()).strip()
        item['title'] = Selector(response).css('.core_title_txt::text').extract_first()
        item['post_time'] = self._fill_time(
            post
            .css('.post-tail-wrap span.tail-info:last-child::text')
            .extract_first() or
            post.css('.p_tail li:last-child span')
            .extract_first()# fix 广东吧
        )
        #TODO: time

        return item;

    def _parse_main_post(self, post, response):
        """TODO: Docstring for _parse_main_post.

        :post: TODO
        :returns: TODO

        """
        item = self._parse_general_post(post, response)
        item['id'] = response.meta['post_id']
        item['type'] = 'MAIN'

        return item;

    def start_requests(self):
        """entry for generating all requests
        :returns: TODO

        """
        try:
            i = 0
            step = 50
            while True:
                rows = self._query_posts(i, step)
                if rows:
                    for row in rows:
                        logging.debug("an post's id: %r" % row[0])
                        post_id = str(row[0])
                        yield Request('http://tieba.baidu.com/p/' + post_id, callback=self.parse, meta={'post_id': post_id})
                    i = i + step
                else:
                    break
        except Exception, e:
            raise e
        #yield Request('http://tieba.baidu.com/p/' + '737767258', callback=self.parse, meta={'post_id': 737767258})

    def parse(self, response):
        """TODO: Docstring for parse.
        :returns: TODO

        """
        posts = Selector(response).css('.p_postlist .l_post')

        for i, post in enumerate(posts):
            if i == 0:
                yield self._parse_main_post(post, response)
            else:
                item = self._parse_reply(post, response)
                yield item

                if item['reply_num'] != 0:# 评论数
                    self._parse_comments(post)





