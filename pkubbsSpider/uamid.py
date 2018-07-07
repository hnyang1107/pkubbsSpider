import random
from pkubbsSpider.settings import UAPOOL
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware

class Uamid(UserAgentMiddleware):
    # 通过设置User-Agent池改变所用报头
    def __init__(self,user_agent = ''):
        self.user_agent = user_agent
        
        
    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        print("当前使用的user-agent:"+thisua)
        request.headers.setdefault('User-Agent', thisua)