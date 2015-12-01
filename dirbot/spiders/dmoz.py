#coding=utf-8
import scrapy
from cookieSpider import CookieSpider as Spider
from scrapy.selector import Selector

from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://tieba.baidu.com/f?kw=阅兵"
    ]


    def parse_next_page(self, response):
        sel = Selector(response)
        sites = sel.xpath('//ul[@id="thread_list"]/li')
        items = []

        for site in sites:
            item = Website()
            #extract方法的是数组，现在只取第一个元素，再去掉首尾的空白和回车
            item['name'] = site.css('div.threadlist_title a::text').extract()[0].strip()
            item['description'] = site.css('div.threadlist_text div::text').extract()[0].strip()
            items.append(item)

        return items

    def parse(self, response):
        globalCookie = self.getCookies()
        #for url in response.css("#frs_list_pager a::attr('href')").extract():
        for url in ["http://tieba.baidu.com/f?kw=%E9%98%85%E5%85%B5&ie=utf-8&pn=50"]:
            #百度这里给的是URL
            yield scrapy.Request(url, callback=self.parse_next_page, cookies=globalCookie)

