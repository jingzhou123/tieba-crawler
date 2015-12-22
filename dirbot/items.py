#coding=utf-8
from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class Tieba(Item):
    name = Field()
    admin_num = Field() #贴吧吧务
    members_num = Field() #关注数
    posts_num = Field() #帖子数
    slogan = Field() #贴吧标语
    dir_name = Field() #一个贴巴的所属目录（和分类有关）
    admin_names = Field()

class Post(Item):
    author_name = Field()
    body = Field()
    id = Field()
    post_time = Field()
    reply_num = Field()
    tieba_name = Field()
    title = Field()

class Reply(Item):
    author_name = Field()
    body = Field()
    id = Field()
    author_id = Field()
    post_time = Field()
    reply_num = Field()
    title = Field()
    type = Field()# 如果是'MAIN'说明是一个主贴
    post_id = Field()# 记录是哪个主贴的回复

class Comment(Item):
    author_name = Field()
    body = Field()
    id = Field()
    post_time = Field()
    reply_id = Field()# 记录是哪个回复评论

class UserFollowTiebaRel(Item):
    user_name = Field()
    tieba_name = Field()

class User(Item):
    id = Field()
    baidu_id = Field()
    name = Field()
    admin_type = Field()
    following_num = Field()
    followed_num = Field()
    following_tieba_name_array = Field()
    tieba_age = Field()
    posts_num = Field()




