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
## 提供了哪些爬虫：
1. tieba: 提供贴吧的一般性信息
1. post: 贴吧内发表的主贴
1. reply: 主贴的回复
1. comment: 回复的回复(评论)
1. user_post, user_reply, user_comment: 通过主题贴、回复和评论取得的用户名来爬用户的详细信息
1. user_fan, user_follow: 通过粉丝关系和关注关系爬粉丝或关注的用户详情
1. fan, follow: 爬每一个用户的关注和粉丝，只有用户名
## 使用方法
`scrapy crawl 名称 2>&1 | tee -a tb.log`
## 依赖：
每个爬虫在运行前最好先运行它依赖的爬虫
1. tieba []
1. post [tieba]
1. reply [post]
1. comment [reply]
1. member [tieba]
1. user_member [member]
1. user_fan [fan]
1. user_follow [follow]
1. user_comment [comment]
1. user_post [post]
1. fan [user_post user_reply user_comment member]
1. follow [user_post user_reply user_comment member]
