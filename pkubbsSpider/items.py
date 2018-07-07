# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 区 (Region) > 板块(Board) > 帖子组(Thread) > 帖子(Post)


class PkubbsspiderItem(scrapy.Item):
    
    
    board_url = scrapy.Field() #板块url链接 
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