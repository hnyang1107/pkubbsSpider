# pkubbsSpider: 北大未名BBS爬虫（https://bbs.pku.edu.cn）
## scrapy框架
- 初始页为区域页（例如：https://bbs.pku.edu.cn/v2/board.php?bid=621）
- 4层参数传递
- 用Cookies传递实现登陆，需开启COOKIES_ENABLED = True
- 设置代理池实现反爬虫（uamid.py）
- 下载间隔时间0.25s，DOWNLOAD_DELAY = 0.25
- 抓取内容 
``` python
    item.py
    
    board_url  #板块url链接 
    board_name_cn = scrapy.Field() #板块中文名称
    board_name_en = scrapy.Field() #板块英文名称
    
    
    thread_title = scrapy.Field() #帖子组标题
    thread_url = scrapy.Field()  #帖子组链接，帖子组的首页
    thread_page_url = scrapy.Field() #帖子组所在的板块页面的url,在一个板块里，这个帖子组在整个板块的第几页
    
    
    
    post_url = scrapy.Field() #post_card的url
    post_id = scrapy.Field() #发帖人ID
    reply_id = scrapy.Field() #回复对象ID
    content = scrapy.Field() #发帖内容
    post_time = scrapy.Field() #发帖时间 
```
