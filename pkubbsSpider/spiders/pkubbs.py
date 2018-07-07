# -*- coding: utf-8 -*-
import scrapy
from pkubbsSpider.items import PkubbsspiderItem
from scrapy.loader.processors import Join, MapCompose
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest


class PkubbsSpider(scrapy.Spider):
    
    name = 'pkubbs'
    allowed_domains = ['bbs.pku.edu.cn']
    start_url = 'https://bbs.pku.edu.cn/v2/board.php?bid=685' # 修改初始url改变所爬论坛区面
    
    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest'
    }
    
    # 重写了start_requests方法,传递Cookies
    def start_requests(self):
        home_url = self.start_url
        login_cookie={'uid':'****',
                      'skey':'*******' # 在此输入Cookies
                      }
        yield FormRequest(
            url=home_url,cookies=login_cookie,callback=self.parse)
    
                 

    def parse(self, response):
        
        login_username = response.xpath('//span[@data-role="login-username"]/text()')[0].extract()
        if login_username =='guest':
            self.log("以 访客 状态抓取") 
        else:
            self.log("以用户名为 "+login_username+" 状态抓取")
            
        items_1 = []
        selector = Selector(response)
        
        infos = selector.xpath('//div[@class="set"]/div[@class="board-block"]')
        
        for info in infos:
            item = PkubbsspiderItem()
            
            board_url = 'https://bbs.pku.edu.cn/v2/' + info.xpath('a/@href')[0].extract()
            board_name_en = info.xpath('div[@class="left"]/span[contains(@class,"name")]/text()')[0].extract()
            board_name_cn = info.xpath('div[@class="left"]/span[contains(@class,"name")]/text()')[1].extract()
            
            item['board_url'] = board_url
            item['board_name_en'] = board_name_en #.encode('utf8')
            item['board_name_cn'] = board_name_cn
            
            items_1.append(item)
            
        for item in items_1:
            yield Request(url=item['board_url'], meta={'item_1': item}, callback=self.parse_item)
        
        
    
    def parse_item(self,response):
            
            login_username = response.xpath('//span[@data-role="login-username"]/text()')[0].extract() # 检查登陆状态
            if login_username =='guest':
                self.log("以 访客 状态抓取") 
            else:
                self.log("以用户名为 "+login_username+" 状态抓取")
            
            item_1 = response.meta['item_1']  
            
            items = []
            
            board_url_index = response.url
            
            if len(response.xpath('//div[contains(@class,"paging")]/div[last()-1]/text()'))==0: # 此时没有页数导航栏
                num_pages = 1
            else:
                num_pages_r = response.xpath('//div[contains(@class,"paging")]/div[last()-1]/text()')[0].extract()
                num_pages = MapCompose(lambda i: i.replace('/ ',''),int)(num_pages_r)[0]
            
            for page in range(1, num_pages+1):
          
                    
                item = PkubbsspiderItem()
                thread_page_url = board_url_index + "&mode=topic&page=" + str(page)
    
                    
                item['board_url'] = item_1['board_url'] 
                item['board_name_en'] = item_1['board_name_en'] 
                item['board_name_cn'] = item_1['board_name_cn']                        
                item['thread_page_url'] = thread_page_url
                    
                items.append(item)
                    
            
            for item in items:
            # 对列表遍历，回调parse_detail函数 进入下一层url 请求的是每个cate_url_list meta将前两层的数据传递到详情页
                yield Request(url=item['thread_page_url'], meta={'item_2':item},callback=self.parse_detail)

        
        
    def parse_detail(self,response):
        
            login_username = response.xpath('//span[@data-role="login-username"]/text()')[0].extract()
            if login_username =='guest':
                self.log("以 访客 状态抓取") 
            else:
                self.log("以用户名为 "+login_username+" 状态抓取")
            
            item_2 = response.meta['item_2']
            items =[]
            
            selector = Selector(response)
            threads = selector.xpath('//div[contains(@class,"list-item")]')
            
            for thread in threads:
                
                item = PkubbsspiderItem()
                
                item['board_url'] = item_2['board_url']
                item['board_name_en'] = item_2['board_name_en']
                item['board_name_cn'] = item_2['board_name_cn']
                item['thread_page_url'] = item_2['thread_page_url']
                
                thread_url = 'https://bbs.pku.edu.cn/v2/' + thread.xpath('a/@href')[0].extract()
                
                    
                item['thread_url'] = thread_url
                item['thread_title'] = thread.xpath('div[contains(@class,"title-cont")]/div[@class="title l limit"]/text()')[0].extract()
                self.log(item['thread_title'])
                self.log(item['thread_page_url'])
                
                items.append(item)
                
            for item in items:
                yield Request(url=item['thread_url'], meta={'item_3':item},callback=self.parse_detail_2)
                
                
        
    def parse_detail_2(self, response):
        
            login_username = response.xpath('//span[@data-role="login-username"]/text()')[0].extract()
            if login_username =='guest':
                self.log("以 访客 状态抓取") 
            else:
                self.log("以用户名为 "+login_username+" 状态抓取")
        
            item_3 = response.meta['item_3']
            items = []
            post_url_index = response.url
            
            if len(response.xpath('//div[contains(@class,"paging")]/div[last()-1]/text()'))==0:
                num_pages = 1
            else:
                num_pages_r = response.xpath('//div[contains(@class,"paging")]/div[last()-1]/text()')[0].extract()
                num_pages = MapCompose(lambda i: i.replace('/ ',''),int)(num_pages_r)[0]
            
            for page in range(1, num_pages+1):
                
                item = PkubbsspiderItem()  
                    
                item['board_url'] = item_3['board_url']
                item['board_name_en'] = item_3['board_name_en']
                item['board_name_cn'] = item_3['board_name_cn']
                item['thread_url'] = item_3['thread_url']
                item['thread_page_url'] = item_3['thread_page_url']
                item['thread_title'] = item_3['thread_title']
                
                post_url = post_url_index + "&page=" + str(page)
                
                    
                item['post_url'] = post_url
                
                items.append(item)
                
            for item in items:
                yield Request(url=item['post_url'], meta={'item_4':item},callback=self.parse_detail_3)
                
                
    
    
    def parse_detail_3(self, response):
        
            login_username = response.xpath('//span[@data-role="login-username"]/text()')[0].extract()
            if login_username =='guest':
                self.log("以 访客 状态抓取") 
            else:
                self.log("以用户名为 "+login_username+" 状态抓取")
        
            item_4 = response.meta['item_4']
            
            selector = Selector(response)
            post_cards = selector.xpath('//div[@class="post-card"]')
            
            for post_card in post_cards:
                
                item = PkubbsspiderItem()
                
                item['board_url'] = item_4['board_url']
                item['board_name_en'] = item_4['board_name_en']
                item['board_name_cn'] = item_4['board_name_cn']
                item['thread_url'] = item_4['thread_url']
                item['thread_page_url'] = item_4['thread_page_url']
                item['thread_title'] = item_4['thread_title']
                item['post_url'] = item_4['post_url']
                
                item['post_id'] = post_card.xpath('div[@class="post-owner"]/p[@class="username"]/a/text()')[0].extract()
                item['content'] = Join()(post_card.xpath('div[@class="post-main"]/div[@class="content"]/div[@class="body file-read image-click-view"]/p[not(@class)]/text()').extract())
                
                reply_id_r = post_card.xpath('div[@class="post-main"]/div[@class="content"]/div[@class="body file-read image-click-view"]/p[@class="quotehead"]/text()')
                
                if len(reply_id_r) == 0:
                    item["reply_id"] = ''    
                else:
                    item["reply_id"] = reply_id_r.re('(.*)\s\(')[0]
                    
                item['post_time'] = post_card.xpath('div[@class="post-main"]/div[@class="operations"]/div[@class="right"]/div[@class="sl-triangle-container"]/span/span/text()').re('.*于(.*)')[0]
                
                yield item     