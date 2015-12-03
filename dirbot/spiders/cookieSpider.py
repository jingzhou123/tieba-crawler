from scrapy.spiders import Spider

class CookieSpider(Spider):
    def getCookies(self):
        """TODO: Docstring for getCookies.

        :f: TODO
        :returns: TODO

        """
        return {
            "BDUSS": self.settings.get('BDUSS'),
            "BAIDUID": self.settings.get('BAIDUID'),
            "TIEBA_USERTYPE": self.settings.get('TIEBA_USERTYPE'),
            "TIEBAUID": self.settings.get('TIEBAUID'),
            "LONGID": self.settings.get('LONGID')
        }
