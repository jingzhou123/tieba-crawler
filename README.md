# tieba-crawler
## 满足下列查询需求：
1. 一个吧的所有关注者（会员）
1. 一个吧的所有帖子
1. 一个用户关注的所有贴吧
1. 一个用户关注的其它所有用户
1. 一个用户的所有粉丝
1. 一个贴吧的所有文章
1. 一个文章(回复)的所有回复(所有回复中互相回复的帖子全算对楼主的回复)
1. 一个文章的所有回复者
## 使用方法
`scrapy crawl 名称 2>&1 | tee -a tb.log`
## 依赖：
每个爬虫在运行前最好先运行它依赖的爬虫
tieba []
post [tieba]
reply [post]
comment [reply]
member [tieba]
user [user_comment, user_post, user_reply]
fan [user]
follow [user]
user_fan [fan]
user_follow [follow]
