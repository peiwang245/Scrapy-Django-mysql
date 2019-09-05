import scrapy
from datetime import datetime
from  ..items import CallBidItem
import re
import time
# from django.utils import timezone as datetime

class CallBidSpider(scrapy.spiders.Spider):
    name = "callbidVcq"
    allow_domains = ["cqjsxx.com"]
    start_urls = ['http://www.cqjsxx.com/webcqjg/GcxxFolder/notice.aspx']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    Headers = {'User-Agent:':user_agent}


    def parse(self, response):
        # time.sleep(2)
        print("*" * 50)
        bids = response.css('tr[bgcolor]')#css选择器
        item = CallBidItem()
        for bid in bids:
            try:
                nname =re.sub(r'\s+','',re.search(r'target="_blank">(.*?)<',bid.extract(),re.S).group(1))
                district = re.sub(r'\s+', '', re.search(r'title="(.*?)">', bid.extract(), re.S).group(1))
                endRegistration = datetime.strptime(re.search(r'"Center".*?size="2">(.*?)</font>', bid.extract(), re.S).group(1), "%Y/%m/%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                item['name']= nname
                item['district'] = district
                item['endRegistration'] = endRegistration
                item['type'] ='--'
                item['purl']='--'
                item['tenderee']='--'
                item['tenderer']='--'
                item['address']='--'
                item['docnmb']='--'
                item['startaffich']='0000-00-00 00:00:00'
                item['endaffich']=None
                item['startRegistration']=None
                yield item
            except:
                print("正则报错")
                pass
        try:
            VIEWSTATE = response.xpath('//input[@name="__VIEWSTATE"]/@value').extract()[0]
            checkPage = response.xpath('//input[@name="checkPage"]/@value').extract()[0]
            data = {
                "__EVENTTARGET": 'Linkbutton3',
                "__EVENTARGUMENT": '',
                "__VIEWSTATE": VIEWSTATE,
                "SearchName": '',
                "SearchNo": '',
                "txtSqlText": 'FProjectName like ''% %'' and FTNO like ''% %''',
                "checkPage": checkPage,
            }
            print("请求：")
            # time.sleep(2)
            yield scrapy.FormRequest(url = self.start_urls[0], formdata=data, callback=self.parse)
        except:
            print("FormRequest报错")
            pass



