from cookieSpider import CookieSpider
from dbSpider import DbSpider
from scrapy import Request, Selector
from dirbot.items import Reply

class CommentSpider(CookieSpider, DbSpider):

    """crawl a post's reply's comments"""
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

    def parse(self, response):
        """TODO: Docstring for parse.

        :response: TODO
        :returns: TODO

        """
        pass

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
                    yield Request('http://tieba.baidu.com/p/comment?tid=' + str(post_id) + '&pid=' + str(reply_id) + '&pn=1',
                            callback=self.parse,
                            meta={'post_id': post_id, 'reply_id': reply_id})

                i = i + step
            else:
                break



