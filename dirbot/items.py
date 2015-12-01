#coding=utf-8
from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class Tieba(Item):
    name = Field()
    owners = Field() #贴吧吧务
    members_num = Field() #关注数
    posts_num = Field() #帖子数
    slogan = Field() #贴吧标语
    dir_name = Field() #一个贴巴的所属目录（和分类有关）
